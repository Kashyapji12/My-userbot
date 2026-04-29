from gtts import gTTS
import uuid, os

async def tts(text):
    file = f"{uuid.uuid4().hex}.mp3"
    gTTS(text).save(file)
    return file