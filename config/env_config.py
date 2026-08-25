"""Environment configuration.

Resolution order for every value: environment-specific env var (e.g.
``DEV_BASE_URL``) -> flat env var (``BASE_URL``) -> ``config/config.yaml``.

Credentials are read from environment variables / `.env` only. Nothing
sensitive is ever hardcoded here or in `config.yaml`.
"""

import os

import yaml
from dotenv import load_dotenv

_BASE_DIR = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_BASE_DIR)

load_dotenv(dotenv_path=os.path.join(_PROJECT_ROOT, ".env"), override=False)

ENV = os.getenv("ENV", "qa").strip().lower()
IS_PROD = ENV == "prod"

with open(os.path.join(_BASE_DIR, "config.yaml"), encoding="utf-8") as config_file:
    _CONFIG = yaml.safe_load(config_file)

_ENV_CONFIG = _CONFIG.get(ENV)
if _ENV_CONFIG is None:
    raise ValueError(
        f"ENV '{ENV}' not found in config/config.yaml. Available: {sorted(_CONFIG)}"
    )


def _env_value(key, default=""):
    """First non-empty of `<ENV>_<KEY>`, `<KEY>`, then `default`."""
    for name in (f"{ENV.upper()}_{key}", key):
        value = (os.getenv(name) or "").strip()
        if value:
            return value
    return default


BASE_URL = _env_value("BASE_URL", _ENV_CONFIG.get("base_url"))
TIMEOUT = int(_env_value("TIMEOUT", _ENV_CONFIG.get("timeout", 300)))
HEADLESS = _env_value("HEADLESS", "false").lower() in ("1", "true", "yes")
SLOW_MO = int(_env_value("SLOW_MO", "0"))
TRACE_ON = _env_value("TRACE_ON", "false").lower() in ("1", "true", "yes")


def _credentials(persona_prefix, fallback=("", "")):
    """Return the (username, password) pair configured for a persona."""
    return (
        _env_value(f"{persona_prefix}_USERNAME", fallback[0]),
        _env_value(f"{persona_prefix}_PASSWORD", fallback[1]),
    )


# The Windows OS sets a `USERNAME` variable holding the Windows account name,
# so a flat USERNAME is only trusted when it actually looks like a login email.
_legacy_username = os.getenv("USERNAME", "")
if "@" not in _legacy_username:
    _legacy_username = ""
_legacy_password = os.getenv("PASSWORD", "")

STUDENT_USERNAME = (_env_value("STUDENT_USERNAME")
                    or _env_value("TEST_USERNAME")
                    or _legacy_username)
STUDENT_PASSWORD = (_env_value("STUDENT_PASSWORD")
                    or _env_value("TEST_PASSWORD")
                    or _legacy_password)

FACULTY_USERNAME, FACULTY_PASSWORD = _credentials("FACULTY")
RM_USERNAME, RM_PASSWORD = _credentials("RM")
CAREER_BUDDY_USERNAME, CAREER_BUDDY_PASSWORD = _credentials("CAREER_BUDDY")
INSTITUTE_ADMIN_USERNAME, INSTITUTE_ADMIN_PASSWORD = _credentials("INSTITUTE_ADMIN")
# A dedicated mentor account is preferred; the Career Buddy account is kept as a
# fallback because both personas historically shared one login.
MENTOR_USERNAME, MENTOR_PASSWORD = _credentials(
    "MENTOR", (CAREER_BUDDY_USERNAME, CAREER_BUDDY_PASSWORD))

# Zoom sandbox account used by the Settings > Zoom Connect scenarios.
ZOOM_USERNAME, ZOOM_PASSWORD = _credentials("ZOOM")
