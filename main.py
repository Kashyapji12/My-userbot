import os
import asyncio
import importlib
import logging

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION

# logging
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# load plugins
async def load_plugins():
    if not os.path.exists("plugins"):
        return
    for f in os.listdir("plugins"):
        if f.endswith(".py"):
            importlib.import_module(f"plugins.{f[:-3]}")

# log messages
@client.on(events.NewMessage)
async def log_all(e):
    if e.text:
        logging.info(f"{e.sender_id}: {e.text}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🔥 Started as {me.first_name}")

    await load_plugins()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())