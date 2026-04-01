import os, yaml
from dotenv import load_dotenv

# Load .env with preferred path first, then fallback.
base_dir = os.path.dirname(__file__)
dotenv_candidates = [
    os.path.join(base_dir, "..", ".env"),
    os.path.join(base_dir, "..", "utils", ".env", ".env"),
]
for dotenv_path in dotenv_candidates:
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path, override=False)
        break

ENV = os.getenv("ENV", "qa")

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)
env = config.get(ENV)
if env is None:
    raise ValueError(f"ENV '{ENV}' not found in config/config.yaml")


def _env_key(key):
    """Generate environment-specific variable name (e.g., DEV_BASE_URL)."""
    return f"{ENV.upper()}_{key}"


def _pick(*values):
    """Return first non-empty value from list."""
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                return cleaned
            continue
        return value
    return ""


# BASE_URL and TIMEOUT with environment-specific override support
base_url_env = _env_key("BASE_URL")
base_url_from_env = (os.getenv(base_url_env) or os.getenv("BASE_URL") or "").strip()
BASE_URL = base_url_from_env or env.get("base_url")

timeout_env = _env_key("TIMEOUT")
timeout_override = os.getenv(timeout_env) or os.getenv("TIMEOUT")
TIMEOUT = int(timeout_override) if timeout_override else env.get("timeout", 300)

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
legacy_username = os.getenv("USERNAME")
if legacy_username and "@" not in legacy_username:
    legacy_username = None

legacy_password = os.getenv("PASSWORD")

# Avoid Windows OS USERNAME collision (it usually contains account name, not login email).
# Prefer explicit test env vars and fallback to config.yaml/legacy email-like username.
# KEEP ORIGINAL LOGIC - Do not change USERNAME/PASSWORD resolution
USERNAME = os.getenv("STUDENT_USERNAME") or os.getenv("TEST_USERNAME") or legacy_username or env.get("username")
PASSWORD = os.getenv("STUDENT_PASSWORD") or os.getenv("TEST_PASSWORD") or legacy_password or env.get("password")

# Persona-specific credentials - check env-specific names first (DEV_*, PROD_*), then fall back to flat names
# This allows different credentials per environment while maintaining backward compatibility
FACULTY_USERNAME = os.getenv(_env_key("FACULTY_USERNAME")) or os.getenv("FACULTY_USERNAME") or ""
FACULTY_PASSWORD = os.getenv(_env_key("FACULTY_PASSWORD")) or os.getenv("FACULTY_PASSWORD") or ""
RM_USERNAME = os.getenv(_env_key("RM_USERNAME")) or os.getenv("RM_USERNAME") or ""
RM_PASSWORD = os.getenv(_env_key("RM_PASSWORD")) or os.getenv("RM_PASSWORD") or ""
CAREER_BUDDY_USERNAME = os.getenv(_env_key("CAREER_BUDDY_USERNAME")) or os.getenv("CAREER_BUDDY_USERNAME") or ""
CAREER_BUDDY_PASSWORD = os.getenv(_env_key("CAREER_BUDDY_PASSWORD")) or os.getenv("CAREER_BUDDY_PASSWORD") or ""
INSTITUTE_ADMIN_USERNAME = os.getenv(_env_key("INSTITUTE_ADMIN_USERNAME")) or os.getenv("INSTITUTE_ADMIN_USERNAME") or ""
INSTITUTE_ADMIN_PASSWORD = os.getenv(_env_key("INSTITUTE_ADMIN_PASSWORD")) or os.getenv("INSTITUTE_ADMIN_PASSWORD") or ""
