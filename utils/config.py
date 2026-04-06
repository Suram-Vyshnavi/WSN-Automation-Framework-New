import os
from config.env_config import (
    BASE_URL as ENV_BASE_URL,
    USERNAME as ENV_USERNAME,
    PASSWORD as ENV_PASSWORD,
    FACULTY_USERNAME as ENV_FACULTY_USERNAME,
    FACULTY_PASSWORD as ENV_FACULTY_PASSWORD,
    RM_USERNAME as ENV_RM_USERNAME,
    RM_PASSWORD as ENV_RM_PASSWORD,
    CAREER_BUDDY_USERNAME as ENV_CAREER_BUDDY_USERNAME,
    CAREER_BUDDY_PASSWORD as ENV_CAREER_BUDDY_PASSWORD,
    INSTITUTE_ADMIN_USERNAME as ENV_INSTITUTE_ADMIN_USERNAME,
    INSTITUTE_ADMIN_PASSWORD as ENV_INSTITUTE_ADMIN_PASSWORD,
)


class Config:
    BASE_URL = ENV_BASE_URL

    # Keep existing student variable names for backward compatibility.
    USERNAME_INPUT = ENV_USERNAME
    PASSWORD_INPUT = ENV_PASSWORD
    USERNAME = USERNAME_INPUT
    PASSWORD = PASSWORD_INPUT

    # New persona-specific variable names.
    FACULTY_USERNAME_INPUT = ENV_FACULTY_USERNAME
    FACULTY_PASSWORD_INPUT = ENV_FACULTY_PASSWORD
    RM_USERNAME_INPUT = ENV_RM_USERNAME
    RM_PASSWORD_INPUT = ENV_RM_PASSWORD
    CAREER_BUDDY_USERNAME_INPUT = ENV_CAREER_BUDDY_USERNAME
    CAREER_BUDDY_PASSWORD_INPUT = ENV_CAREER_BUDDY_PASSWORD
    INSTITUTE_ADMIN_USERNAME_INPUT = ENV_INSTITUTE_ADMIN_USERNAME
    INSTITUTE_ADMIN_PASSWORD_INPUT = ENV_INSTITUTE_ADMIN_PASSWORD

    MESSAGE_TEXT = "hello"

    # Persona-wise credentials. Defaults can be overridden by environment vars.
    CREDENTIALS = {
        "student": {
            # Use env_config-resolved values so ENV=prod picks PROD_STUDENT_* first.
            "username": USERNAME_INPUT,
            "password": PASSWORD_INPUT,
        },
        "faculty": {
            "username": FACULTY_USERNAME_INPUT,
            "password": FACULTY_PASSWORD_INPUT,
        },
        "rm": {
            "username": RM_USERNAME_INPUT,
            "password": RM_PASSWORD_INPUT,
        },
        "career_buddy": {
            "username": CAREER_BUDDY_USERNAME_INPUT,
            "password": CAREER_BUDDY_PASSWORD_INPUT,
        },
        "institute_admin": {
            "username": INSTITUTE_ADMIN_USERNAME_INPUT,
            "password": INSTITUTE_ADMIN_PASSWORD_INPUT,
        },
    }

    @classmethod
    def get_persona(cls):
        return os.getenv("PERSONA", "student").strip().lower()

    @classmethod
    def get_credentials(cls, persona=None):
        selected = (persona or cls.get_persona()).strip().lower()
        if selected not in cls.CREDENTIALS:
            raise ValueError(f"Unsupported persona: {selected}")

        creds = cls.CREDENTIALS[selected]
        if not creds["username"] or not creds["password"]:
            raise ValueError(
                f"Missing credentials for persona '{selected}'. "
                "Set persona env vars (e.g. STUDENT_*, FACULTY_*, RM_*, CAREER_BUDDY_*, INSTITUTE_ADMIN_*) "
                "or update utils/config.py"
            )
        return creds["username"], creds["password"]
