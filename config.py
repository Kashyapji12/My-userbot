import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

SUDO_USERS = [
    int(x) for x in os.getenv("SUDO", "").split(",") if x.strip().isdigit()
]