import os, yaml
from dotenv import load_dotenv

# Load .env with preferred path first, then fallback.
base_dir = os.path.dirname(__file__)
dotenv_candidates = [
    os.path.join(base_dir, "..", "utils", ".env", ".env"),
    os.path.join(base_dir, "..", ".env"),
]
for dotenv_path in dotenv_candidates:
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path, override=False)
        break

ENV = os.getenv("ENV", "qa")

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)
env = config[ENV]

BASE_URL = os.getenv("BASE_URL", env["base_url"])
TIMEOUT = env["timeout"]
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
legacy_username = os.getenv("USERNAME")
if legacy_username and "@" not in legacy_username:
    legacy_username = None

legacy_password = os.getenv("PASSWORD")

# Avoid Windows OS USERNAME collision (it usually contains account name, not login email).
# Prefer explicit test env vars and fallback to config.yaml/legacy email-like username.
USERNAME = os.getenv("STUDENT_USERNAME") or os.getenv("TEST_USERNAME") or legacy_username or env.get("username")
PASSWORD = os.getenv("STUDENT_PASSWORD") or os.getenv("TEST_PASSWORD") or legacy_password or env.get("password")

# Persona-specific credentials
FACULTY_USERNAME = os.getenv("FACULTY_USERNAME", "")
FACULTY_PASSWORD = os.getenv("FACULTY_PASSWORD", "")
CAREER_BUDDY_USERNAME = os.getenv("CAREER_BUDDY_USERNAME", "")
CAREER_BUDDY_PASSWORD = os.getenv("CAREER_BUDDY_PASSWORD", "")
INSTITUTE_ADMIN_USERNAME = os.getenv("INSTITUTE_ADMIN_USERNAME", "")
INSTITUTE_ADMIN_PASSWORD = os.getenv("INSTITUTE_ADMIN_PASSWORD", "")
