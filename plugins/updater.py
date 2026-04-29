from main import client
from telethon import events
import os, sys

@client.on(events.NewMessage(pattern=r"\.update", outgoing=True))
async def updater(e):
    await e.edit("🔄 Updating from GitHub...")

    os.system("git pull")

    await e.edit("♻️ Restarting...")
    os.execv(sys.executable, ["python"] + sys.argv)