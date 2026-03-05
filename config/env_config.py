import os, yaml
from dotenv import load_dotenv

# Force load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

ENV = os.getenv("ENV", "qa")

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)
env = config[ENV]

BASE_URL = os.getenv("BASE_URL", env["base_url"])
TIMEOUT = env["timeout"]
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
USERNAME = os.getenv("USERNAME", env.get("username"))
PASSWORD = os.getenv("PASSWORD", env.get("password"))
