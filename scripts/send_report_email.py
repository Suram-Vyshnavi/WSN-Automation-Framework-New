"""
Generate (or reuse) the executive HTML report, derive the execution statistics
from the very same Allure results, compose the stakeholder summary email and
send it through Microsoft Graph.

Designed to run AFTER the tests, whatever their exit code — a failing suite is
exactly the run people most need the mail for.

Examples
--------
    # Local: reuse the report the combined matrix run just produced
    python scripts/send_report_email.py --env prod

    # Local dry run: write the email to reports/email-preview.html, send nothing
    python scripts/send_report_email.py --env prod --dry-run

    # CI: merge the per-persona allure-results artifacts first
    python scripts/send_report_email.py --merge-dir reports/_artifacts --env prod
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    for _candidate in (PROJECT_ROOT / ".env", PROJECT_ROOT / "utils" / ".env" / ".env"):
        if _candidate.exists():
            load_dotenv(dotenv_path=str(_candidate), override=False)
            break
except Exception:
    pass

from utils.email_body import build_email_html, build_subject  # noqa: E402
from utils.executive_report import PERSONA_PRETTY  # noqa: E402
from utils.report_stats import collect_run_stats  # noqa: E402

DEFAULT_RESULTS_DIR = PROJECT_ROOT / "reports" / "allure-results-combined"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "reports" / "allure-report-combined"
DEFAULT_REPORT = DEFAULT_REPORT_DIR / "executive-dashboard-combined.html"
CONFIG_FILE = PROJECT_ROOT / "config" / "email_config.yaml"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
def _split(value: str) -> list[str]:
    return [part.strip() for part in (value or "").replace(";", ",").split(",") if part.strip()]


def load_email_config() -> dict:
    """config/email_config.yaml, with environment variables taking precedence."""
    cfg = {}
    if CONFIG_FILE.exists():
        try:
            import yaml
            cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
        except Exception as exc:  # a broken config must not sink the run
            print(f"WARN: could not read {CONFIG_FILE.name} ({exc}); using defaults.")

    cfg.setdefault("product", "WSN")
    cfg.setdefault("application", "Web Automation")
    cfg.setdefault("signature", "")
    cfg.setdefault("subject_template", "{product} {env_short} {application} – Summary/Report")
    cfg.setdefault("attachment_name", "all_personas_{env}_report.html")

    for key, var in (("product", "EMAIL_PRODUCT"),
                     ("application", "EMAIL_APPLICATION"),
                     ("signature", "EMAIL_SIGNATURE_NAME"),
                     ("subject_template", "EMAIL_SUBJECT_TEMPLATE"),
                     ("attachment_name", "EMAIL_ATTACHMENT_NAME")):
        if os.getenv(var):
            cfg[key] = os.getenv(var)

    groups = cfg.get("recipients") or {}
    for key, var in (("teammates", "EMAIL_TEAMMATES"),
                     ("manager", "EMAIL_MANAGER"),
                     ("cto", "EMAIL_CTO"),
                     ("cc", "EMAIL_CC")):
        if os.getenv(var):
            groups[key] = _split(os.getenv(var))

    to = []
    for key in ("teammates", "manager", "cto"):
        for address in (groups.get(key) or []):
            if address not in to:
                to.append(address)
    if os.getenv("EMAIL_TO"):  # a flat override replaces every group
        to = _split(os.getenv("EMAIL_TO"))

    cc = [a for a in (groups.get("cc") or []) if a not in to]

    cfg["to"] = to
    cfg["cc"] = cc
    return cfg


# ---------------------------------------------------------------------------
# CI helper: merge per-persona allure results into one combined directory
# ---------------------------------------------------------------------------
def merge_results(merge_dir: Path, combined_dir: Path, default_env: str) -> int:
    """Merge downloaded ``allure-results-*`` folders into ``combined_dir``.

    Mirrors run_tests._merge_run_into_combined: every ``*-result.json`` is
    re-tagged with its environment + persona_role so the executive dashboard and
    the email can break results down per flow. Attachment/container files keep
    their original names so their ``source`` references still resolve.
    """
    merge_dir = Path(merge_dir)
    if not merge_dir.exists():
        print(f"WARN: merge dir {merge_dir} does not exist; nothing to merge.")
        return 0

    combined_dir.mkdir(parents=True, exist_ok=True)

    # Either merge_dir itself holds results, or it holds one folder per artifact.
    sources = [d for d in merge_dir.iterdir() if d.is_dir()] or []
    if any(merge_dir.glob("*-result.json")):
        sources.append(merge_dir)

    merged = 0
    for source in sources:
        if not any(source.glob("*-result.json")):
            continue
        # "allure-results-prod-student" -> env=prod, persona=student
        # "allure-results-student"      -> env=<default>, persona=student
        parts = source.name.replace("allure-results", "").strip("-_").split("-")
        parts = [p for p in parts if p]
        env_name, persona = default_env, ""
        if len(parts) >= 2 and parts[0] in ("dev", "qa", "prod", "preprod"):
            env_name, persona = parts[0], "_".join(parts[1:])
        elif parts:
            persona = "_".join(parts)
        pretty_role = PERSONA_PRETTY.get(persona, persona.replace("_", " ").title()) if persona else ""

        for item in source.iterdir():
            if not item.is_file():
                continue
            destination = combined_dir / item.name
            if item.name.endswith("-result.json"):
                try:
                    data = json.loads(item.read_text(encoding="utf-8"))
                    labels = [l for l in data.get("labels", [])
                              if l.get("name") not in ("environment", "persona_role")]
                    labels.append({"name": "environment", "value": env_name})
                    if pretty_role:
                        labels.append({"name": "persona_role", "value": pretty_role})
                    data["labels"] = labels
                    destination.write_text(json.dumps(data), encoding="utf-8")
                    merged += 1
                    continue
                except Exception:
                    pass  # fall through to a verbatim copy
            shutil.copy2(item, destination)
        print(f"  merged {source.name}  (env={env_name}, persona={persona or '—'})")

    print(f"Merged {merged} scenario result file(s) into {combined_dir}")
    return merged


# ---------------------------------------------------------------------------
# Report generation status (evaluated independently of test status)
# ---------------------------------------------------------------------------
def ensure_report(results_dir: Path, report_path: Path, env_name: str,
                  persona: str, regenerate: bool) -> tuple[bool, Path | None]:
    """Return (report_generated, path). Never raises — a report failure is a
    reportable outcome, not a crash."""
    if report_path.exists() and not regenerate:
        print(f"Reusing existing report: {report_path}")
        return True, report_path
    try:
        from utils.executive_report import generate_executive_dashboard
        produced = generate_executive_dashboard(
            results_dir, report_path, persona=persona,
            extra_meta={"env": env_name},
        )
        produced = Path(produced)
        if produced.exists() and produced.stat().st_size > 0:
            print(f"Report generated: {produced}")
            return True, produced
        print("ERROR: report generation produced no output file.")
        return False, None
    except Exception as exc:
        print(f"ERROR: report generation failed: {exc}")
        return False, None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Email the automation execution summary via Microsoft Graph")
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR),
                        help="Allure results directory to read statistics from")
    parser.add_argument("--merge-dir", default="",
                        help="Directory of downloaded per-persona allure-results folders to merge first (CI)")
    parser.add_argument("--report", default=str(DEFAULT_REPORT),
                        help="HTML report to attach (generated when missing)")
    parser.add_argument("--regenerate", action="store_true",
                        help="Regenerate the HTML report even if it already exists")
    parser.add_argument("--env", default=os.getenv("ENV", "prod"),
                        help="Environment label used when results carry none")
    parser.add_argument("--persona", default=os.getenv("PERSONA", "combined"))
    parser.add_argument("--to", default="", help="Override To: recipients (comma separated)")
    parser.add_argument("--cc", default="", help="Override Cc: recipients (comma separated)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Write the composed email to disk instead of sending it")
    parser.add_argument("--preview-out", default=str(PROJECT_ROOT / "reports" / "email-preview.html"))
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    report_path = Path(args.report)
    env_name = (args.env or "prod").strip().lower()

    if args.merge_dir:
        merge_results(Path(args.merge_dir), results_dir, env_name)

    if not results_dir.exists():
        print(f"ERROR: results directory not found: {results_dir}")

    # 1) Report generation — status tracked separately from test outcomes.
    report_generated, attach_path = ensure_report(
        results_dir, report_path, env_name, args.persona, args.regenerate)

    # 2) Statistics from the same results the report was built from.
    stats = collect_run_stats(results_dir, env=env_name, persona=args.persona)

    # 3) Compose.
    cfg = load_email_config()
    if args.to:
        cfg["to"] = _split(args.to)
    if args.cc:
        cfg["cc"] = _split(args.cc)

    delivered_name = ""
    attachments, attachment_names = [], {}
    if report_generated and attach_path:
        delivered_name = str(cfg["attachment_name"]).format(
            env=env_name,
            env_short=(stats.get("env_short") or env_name).lower().replace(" + ", "-"),
            date=stats.get("duration_human", ""),
        )
        attachments = [attach_path]
        attachment_names = {str(attach_path): delivered_name}

    subject = build_subject(stats, cfg)
    body = build_email_html(stats, cfg, report_generated=report_generated,
                            attachment_name=delivered_name or None)

    print("\n================ EMAIL SUMMARY ================")
    print(f"  Subject     : {subject}")
    print(f"  To          : {', '.join(cfg['to']) or '(none configured)'}")
    print(f"  Cc          : {', '.join(cfg['cc']) or '—'}")
    print(f"  Scenarios   : {stats['total']} total | {stats['passed']} passed | "
          f"{stats['failed']} failed | {stats['broken']} error | {stats['skipped']} skipped")
    print(f"  Pass %      : {stats['pass_pct']}%")
    print(f"  Steps       : {stats['steps_display']}")
    print(f"  Duration    : {stats['duration_human']}")
    print(f"  Environment : {stats['env_display']}")
    print(f"  Report       : {'generated' if report_generated else 'NOT generated'}")
    print(f"  Attachment  : {delivered_name or '(none)'}")
    print("===============================================\n")

    # 4) Deliver.
    if args.dry_run:
        preview = Path(args.preview_out)
        preview.parent.mkdir(parents=True, exist_ok=True)
        preview.write_text(body, encoding="utf-8")
        print(f"Dry run — email body written to {preview} (nothing sent).")
        return 0

    from utils.graph_mailer import GraphMailer, GraphMailerError
    mailer = GraphMailer()
    configured, missing = mailer.is_configured()
    if not configured:
        print(f"WARN: Microsoft Graph not configured (missing: {', '.join(missing)}). Email not sent.")
        return 0
    if not cfg["to"]:
        print("WARN: no recipients configured (EMAIL_TO / config/email_config.yaml). Email not sent.")
        return 0

    try:
        mailer.send(subject=subject, html_body=body, to=cfg["to"], cc=cfg["cc"],
                    attachments=attachments, attachment_names=attachment_names)
        print(f"Email sent to {len(cfg['to'])} recipient(s)"
              + (f" with attachment {delivered_name}" if delivered_name else " (no attachment)"))
        return 0
    except GraphMailerError as exc:
        print(f"ERROR: failed to send email: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
