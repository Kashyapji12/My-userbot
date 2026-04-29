import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
ALLOW_GROUP_AI = True
TRIGGER_WORDS = ["bot", "ai", "help"]
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
SUDO_USERS = list(map(int, os.getenv("SUDO", "").split(",")))

CMD = "."