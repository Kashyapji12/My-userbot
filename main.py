import os, importlib, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import *
from core.rate_limit import allowed
from core.memory import update_memory
from core.ai import ai

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def load_plugins():
    for f in os.listdir("plugins"):
        if f.endswith(".py"):
            importlib.import_module(f"plugins.{f[:-3]}")

@client.on(events.NewMessage(incoming=True))
async def smart_ai(e):
    if not e.text or not e.is_private:
        return

    if not allowed(e.sender_id):
        return

    update_memory(e.sender_id, e.text)

    await asyncio.sleep(1.5)  # anti-ban delay
    reply = await ai(e.sender_id, e.text)
    await e.reply(reply)

async def main():
    await client.start()
    print("🔥 ULTRA BOT RUNNING")

    await load_plugins()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())