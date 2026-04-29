from main import client
from telethon import events

GROUP_AI = True

@client.on(events.NewMessage(pattern=r"\.groupai (on|off)", outgoing=True))
async def toggle_group(e):
    global GROUP_AI
    GROUP_AI = e.pattern_match.group(1) == "on"
    await e.edit(f"🤖 Group AI {'ON' if GROUP_AI else 'OFF'}")