from main import client
from telethon import events
import os, sys

@client.on(events.NewMessage(pattern=r"\.restart", outgoing=True))
async def restart(e):
    await e.edit("♻️ Restarting bot...")
    os.execv(sys.executable, ["python"] + sys.argv)