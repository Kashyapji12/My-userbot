import os, importlib, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import *

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 🔌 plugins auto load
async def load_plugins():
    for f in os.listdir("plugins"):
        if f.endswith(".py"):
            importlib.import_module(f"plugins.{f[:-3]}")

async def main():
    await client.start()
    print("🔥 Bot Started")

    await load_plugins()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())