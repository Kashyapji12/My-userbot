import os
import importlib
import asyncio
import logging

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import API_ID, API_HASH, SESSION

# ---------------- LOGGING ---------------- #
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- CLIENT ---------------- #
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


# ---------------- LOAD PLUGINS ---------------- #
async def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            try:
                importlib.import_module(f"plugins.{file[:-3]}")
                logging.info(f"Loaded plugin: {file}")
            except Exception as e:
                logging.error(f"Failed to load {file}: {e}")


# ---------------- GLOBAL LOGGER ---------------- #
@client.on(events.NewMessage)
async def log_messages(event):
    try:
        if event.text:
            logging.info(f"{event.sender_id} | {event.chat_id} : {event.text}")
    except Exception as e:
        logging.error(f"Log error: {e}")


# ---------------- KEEP