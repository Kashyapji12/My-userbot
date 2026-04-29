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
    if not e.text:
        return

    is_private = e.is_private
    is_group = e.is_group

    # --- GROUP CONTROL ---
    if is_group:
        if not ALLOW_GROUP_AI:
            return

        me = await client.get_me()

        is_mention = f"@{me.username}" in e.text if me.username else False
        is_reply = e.is_reply and (await e.get_reply_message()).sender_id == me.id
        has_trigger = any(word in e.text.lower() for word in TRIGGER_WORDS)

        if not (is_mention or is_reply or has_trigger):
            return

    # --- RATE LIMIT ---
    if not allowed(e.sender_id):
        return

    # --- MEMORY ---
    update_memory(e.sender_id, e.text)

    await asyncio.sleep(1.5)

    reply = await ai(e.sender_id, e.text)
    await e.reply(reply)