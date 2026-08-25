"""
Microsoft Graph (Microsoft 365) mail sender.

Uses the OAuth2 **client-credentials** flow — an Azure AD app registration with
the *application* permission ``Mail.Send`` — so the automation can mail from a
service mailbox with no interactive login and no Outlook desktop UI.

Nothing is hardcoded: tenant id, client id, client secret and the sender mailbox
all come from environment variables / GitHub Secrets.

    GRAPH_TENANT_ID        Azure AD directory (tenant) ID
    GRAPH_CLIENT_ID        Application (client) ID of the app registration
    GRAPH_CLIENT_SECRET    Client secret value
    GRAPH_SENDER           UPN / email of the mailbox to send as

Attachments up to ~3 MB are inlined into the sendMail call. Larger ones are
uploaded through a Graph upload session against a draft message, which raises
the ceiling to 150 MB — the executive dashboard grows with embedded
screenshots, so this path matters.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

import requests

GRAPH_ROOT = "https://graph.microsoft.com/v1.0"
LOGIN_ROOT = "https://login.microsoftonline.com"

# Graph rejects a sendMail payload above 4 MB; keep headroom for the base64
# inflation (~33%) and the message body.
INLINE_ATTACHMENT_LIMIT = 3 * 1024 * 1024
# Upload-session chunks must be a multiple of 320 KiB.
UPLOAD_CHUNK = 320 * 1024 * 10


class GraphMailerError(RuntimeError):
    pass


class GraphMailer:
    def __init__(self, tenant_id=None, client_id=None, client_secret=None,
                 sender=None, timeout=60):
        self.tenant_id = (tenant_id or os.getenv("GRAPH_TENANT_ID", "")).strip()
        self.client_id = (client_id or os.getenv("GRAPH_CLIENT_ID", "")).strip()
        self.client_secret = (client_secret or os.getenv("GRAPH_CLIENT_SECRET", "")).strip()
        self.sender = (sender or os.getenv("GRAPH_SENDER", "")).strip()
        self.timeout = timeout
        self._token = None

    # -- configuration ----------------------------------------------------
    def is_configured(self) -> tuple[bool, list[str]]:
        """Return (ok, missing_var_names) so callers can degrade gracefully."""
        missing = [name for name, value in (
            ("GRAPH_TENANT_ID", self.tenant_id),
            ("GRAPH_CLIENT_ID", self.client_id),
            ("GRAPH_CLIENT_SECRET", self.client_secret),
            ("GRAPH_SENDER", self.sender),
        ) if not value]
        return (not missing), missing

    # -- auth -------------------------------------------------------------
    def token(self) -> str:
        if self._token:
            return self._token
        ok, missing = self.is_configured()
        if not ok:
            raise GraphMailerError(f"Missing Graph configuration: {', '.join(missing)}")

        response = requests.post(
            f"{LOGIN_ROOT}/{self.tenant_id}/oauth2/v2.0/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials",
            },
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise GraphMailerError(
                f"Token request failed ({response.status_code}): {response.text[:400]}")
        self._token = response.json().get("access_token", "")
        if not self._token:
            raise GraphMailerError("Token response contained no access_token.")
        return self._token

    def _headers(self, json_body=True) -> dict:
        headers = {"Authorization": f"Bearer {self.token()}"}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    # -- helpers ----------------------------------------------------------
    @staticmethod
    def _recipients(addresses) -> list[dict]:
        return [{"emailAddress": {"address": a}} for a in (addresses or []) if a]

    @staticmethod
    def _content_type(path: Path) -> str:
        suffix = path.suffix.lower()
        return {
            ".html": "text/html",
            ".htm": "text/html",
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".json": "application/json",
            ".txt": "text/plain",
            ".zip": "application/zip",
        }.get(suffix, "application/octet-stream")

    # -- send -------------------------------------------------------------
    def send(self, subject: str, html_body: str, to, cc=None, attachments=None,
             attachment_names=None, save_to_sent=True) -> None:
        """Send an HTML mail with optional file attachments.

        ``attachments``      iterable of file paths
        ``attachment_names`` optional {source_path: delivered_filename} mapping
        """
        to_list = self._recipients(to)
        if not to_list:
            raise GraphMailerError("No recipients configured — refusing to send.")

        paths = [Path(p) for p in (attachments or [])]
        paths = [p for p in paths if p.exists()]
        names = attachment_names or {}
        large = [p for p in paths if p.stat().st_size > INLINE_ATTACHMENT_LIMIT]

        message = {
            "subject": subject,
            "body": {"contentType": "HTML", "content": html_body},
            "toRecipients": to_list,
            "ccRecipients": self._recipients(cc),
        }

        if not large:
            message["attachments"] = [{
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": names.get(str(p), p.name),
                "contentType": self._content_type(p),
                "contentBytes": base64.b64encode(p.read_bytes()).decode("ascii"),
            } for p in paths]
            response = requests.post(
                f"{GRAPH_ROOT}/users/{self.sender}/sendMail",
                headers=self._headers(),
                json={"message": message, "saveToSentItems": save_to_sent},
                timeout=self.timeout,
            )
            if response.status_code not in (200, 202):
                raise GraphMailerError(
                    f"sendMail failed ({response.status_code}): {response.text[:400]}")
            return

        # Large attachment path: draft -> upload session(s) -> send.
        draft = requests.post(
            f"{GRAPH_ROOT}/users/{self.sender}/messages",
            headers=self._headers(), json=message, timeout=self.timeout)
        if draft.status_code not in (200, 201):
            raise GraphMailerError(
                f"Draft creation failed ({draft.status_code}): {draft.text[:400]}")
        message_id = draft.json()["id"]

        for path in paths:
            self._upload_attachment(message_id, path, names.get(str(path), path.name))

        sent = requests.post(
            f"{GRAPH_ROOT}/users/{self.sender}/messages/{message_id}/send",
            headers=self._headers(), timeout=self.timeout)
        if sent.status_code not in (200, 202):
            raise GraphMailerError(f"send failed ({sent.status_code}): {sent.text[:400]}")

    def _upload_attachment(self, message_id: str, path: Path, name: str) -> None:
        size = path.stat().st_size
        session = requests.post(
            f"{GRAPH_ROOT}/users/{self.sender}/messages/{message_id}/attachments/createUploadSession",
            headers=self._headers(),
            json={"AttachmentItem": {
                "attachmentType": "file",
                "name": name,
                "size": size,
                "contentType": self._content_type(path),
            }},
            timeout=self.timeout,
        )
        if session.status_code not in (200, 201):
            raise GraphMailerError(
                f"createUploadSession failed ({session.status_code}): {session.text[:400]}")
        upload_url = session.json()["uploadUrl"]

        with path.open("rb") as handle:
            start = 0
            while start < size:
                chunk = handle.read(UPLOAD_CHUNK)
                if not chunk:
                    break
                end = start + len(chunk) - 1
                put = requests.put(
                    upload_url,
                    headers={
                        "Content-Length": str(len(chunk)),
                        "Content-Range": f"bytes {start}-{end}/{size}",
                    },
                    data=chunk,
                    timeout=self.timeout,
                )
                if put.status_code not in (200, 201, 202):
                    raise GraphMailerError(
                        f"Attachment chunk upload failed ({put.status_code}): {put.text[:400]}")
                start = end + 1

