from main import client
from telethon import events
from core.voice import tts
import os

@client.on(events.NewMessage(pattern=r"\.tts (.*)", outgoing=True))
async def tts_cmd(e):
    text = e.pattern_match.group(1)
    file = await tts(text)

    await client.send_file(e.chat_id, file, voice_note=True)
    os.remove(file)