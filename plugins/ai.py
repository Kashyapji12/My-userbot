from main import client
from telethon import events
from core.ai import ai

@client.on(events.NewMessage(pattern=r"\.ai (.*)", outgoing=True))
async def ai_cmd(e):
    q = e.pattern_match.group(1)
    await e.edit(await ai(q))