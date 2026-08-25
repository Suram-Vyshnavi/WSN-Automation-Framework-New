"""Test configuration: personas, credentials and shared test data.

Credentials come from environment variables / `.env` only (see
`config/env_config.py`). Nothing sensitive is hardcoded here - a missing
credential raises a clear error instead of silently falling back to a
committed account.
"""

import os

from config import env_config


class Config:
    BASE_URL = env_config.BASE_URL
    TIMEOUT = env_config.TIMEOUT
    HEADLESS = env_config.HEADLESS
    SLOW_MO = env_config.SLOW_MO
    TRACE_ON = env_config.TRACE_ON

    # Shared test data.
    MESSAGE_TEXT = "hello"

    DEFAULT_PERSONA = "student"

    CREDENTIALS = {
        "student": (env_config.STUDENT_USERNAME, env_config.STUDENT_PASSWORD),
        "faculty": (env_config.FACULTY_USERNAME, env_config.FACULTY_PASSWORD),
        "rm": (env_config.RM_USERNAME, env_config.RM_PASSWORD),
        "career_buddy": (env_config.CAREER_BUDDY_USERNAME, env_config.CAREER_BUDDY_PASSWORD),
        "institute_admin": (env_config.INSTITUTE_ADMIN_USERNAME, env_config.INSTITUTE_ADMIN_PASSWORD),
        "mentor": (env_config.MENTOR_USERNAME, env_config.MENTOR_PASSWORD),
        "zoom": (env_config.ZOOM_USERNAME, env_config.ZOOM_PASSWORD),
    }

    @classmethod
    def get_persona(cls):
        """Persona selected for this run (defaults to student)."""
        return os.getenv("PERSONA", cls.DEFAULT_PERSONA).strip().lower()

    @classmethod
    def get_credentials(cls, persona=None):
        """Return (username, password) for a persona.

        Raises when the persona is unknown or its credentials are not
        configured, so a run fails fast with an actionable message instead of
        attempting to log in with blanks.
        """
        selected = (persona or cls.get_persona()).strip().lower()
        if selected not in cls.CREDENTIALS:
            raise ValueError(
                f"Unsupported persona '{selected}'. Known personas: {sorted(cls.CREDENTIALS)}"
            )

        username, password = cls.CREDENTIALS[selected]
        if not username or not password:
            prefix = selected.upper()
            raise ValueError(
                f"Missing credentials for persona '{selected}'. Set {prefix}_USERNAME and "
                f"{prefix}_PASSWORD (or {env_config.ENV.upper()}_{prefix}_USERNAME / "
                f"{env_config.ENV.upper()}_{prefix}_PASSWORD) in the environment or .env file."
            )
        return username, password

    @classmethod
    def has_credentials(cls, persona):
        """True when both a username and a password are configured for `persona`."""
        username, password = cls.CREDENTIALS.get(persona.strip().lower(), ("", ""))
        return bool(username and password)
