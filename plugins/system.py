from main import client
from telethon import events

@client.on(events.NewMessage(pattern=r"\.restart", outgoing=True))
async def restart(e):
    await e.edit("♻️ Restarting...")
    import os, sys
    os.execv(sys.executable, ["python"] + sys.argv)