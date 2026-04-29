from main import client
from telethon import events
import datetime

@client.on(events.NewMessage(pattern=r"\.ping", outgoing=True))
async def ping(e):
    t = datetime.datetime.now()
    await e.edit("⚡")
    ms = (datetime.datetime.now()-t).microseconds/1000
    await e.edit(f"🚀 {ms}ms")

@client.on(events.NewMessage(pattern=r"\.id", outgoing=True))
async def id_cmd(e):
    await e.edit(f"Chat ID: {e.chat_id}")