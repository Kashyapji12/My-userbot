from main import client
from telethon import events

@client.on(events.NewMessage(pattern=r"\.logs", outgoing=True))
async def logs(e):
    await client.send_file(e.chat_id, "logs.txt")