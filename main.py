import os, sys, asyncio, datetime, requests, time, random, io, re
import pytz
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- CONFIGURATION (Directly put your values here) ---
API_ID = 34769008 
API_HASH = "98cc9d9d0750ba94abab2e60de1790a0"
SESSION_STRING = "1BVtsOKEBu3H0HfV72WmonKhUhefSprfgrakObI4WeQElpzNwcFouOgc80BDI3s9AUs4yasFI6eboqRQoZlJPiqZX1Ik7PeU_UXFAlVOizeT_t-LUocVJUcBrtm4QcXbBVO3UsI7ccnmVwRwiuxOyfWGjVG7V5nbANHk0PV-o80N4m7B3Cn1hkarqfZjMK_z68pnaaaUfhfppqPrXWKOEJn4TH5JRtQRirlWgFq4tN-ppnvXOdUJYouFLQP2KnDC8bZVpkzm2SYa1RQNO6LoCdFuPSYgJprJTwLoKR1bTpKy1xOZfgMNgGOTb48qsd7AjUDgVpmNDCDn92wUS7MnS1syJxDEy8fo="
OPENROUTER_KEY = "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" # OpenRouter API Key yahan dalen
# ---------------------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
IST = pytz.timezone('Asia/Kolkata')
# OpenRouter models: google/gemini-2.0-flash-exp:free ya google/gemini-2.0-pro-exp-02-05:free
AI_MODEL = "google/gemini-2.0-flash-exp:free"

# STATE VARIABLES
AUTO_AI = False
ORIGINAL_NAME = ""
ORIGINAL_BIO = ""
AFK_REASON = None
SPAM_FILTER = False

def get_fancy(text):
    n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    f = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    return "".join([f[n.index(c)] if c in n else c for c in text])

# --- OPENROUTER API FUNCTION ---
def get_ai_response(prompt, system_p="You are a smart assistant."):
    if not OPENROUTER_KEY or OPENROUTER_KEY == "VALUE": return "API Key Missing!"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/telegram-userbot", # Optional
    }
    data = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_p},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=15)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI Error: {str(e)}"

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🔥 Bot is Running as {me.first_name}")

    # --- 📚 ALL-IN-ONE HELP ---
    @client.on(events.NewMessage(pattern=r"^[.! ]help", outgoing=True))
    async def help_menu(event):
        h = f"🏆 **{get_fancy('Supreme Userbot Pro')}**\n\n"
        h += "🎭 **CLONE:** `.clone` | `.revert` | `.font`\n"
        h += "🤖 **AI:** `.autoai on/off` | `.ai` | `.tts` | `.debate`\n"
        h += "🛡️ **MOD:** `.antispam on/off` | `.purge` | `.ban`\n"
        h += "😂 **FUN:** `.roast` | `.meme` | `.hack` | `.joke`\n"
        h += "📊 **INFO:** `.id` | `.info` | `.poll` | `.sum`\n"
        h += "🚀 **SYS:** `.ping` | `.alive` | `.afk`"
        await event.edit(h)

    # --- 🎭 ADVANCED CLONE & REVERT ---
    @client.on(events.NewMessage(pattern=r"^[.! ]clone", outgoing=True))
    async def clone_cmd(event):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("`Reply to someone!`")
        await event.edit("🕵️‍♂️ `Cloning Profile...`")
        user = await client.get_entity(reply.sender_id)
        full = await client(functions.users.GetFullUserRequest(user.id))
        
        # Backup
        global ORIGINAL_NAME, ORIGINAL_BIO
        me_full = await client(functions.users.GetFullUserRequest(me.id))
        ORIGINAL_NAME = me.first_name
        ORIGINAL_BIO = me_full.full_user.about or ""

        # Photo
        photos = await client.get_profile_photos(user.id)
        if photos:
            path = await client.download_media(photos[0])
            await client(functions.photos.UploadProfilePhotoRequest(await client.upload_file(path)))
        
        await client(functions.account.UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name or "", about=full.full_user.about or ""))
        await event.edit(f"✅ **Cloned successfully as {user.first_name}!**")

    @client.on(events.NewMessage(pattern=r"^[.! ]revert", outgoing=True))
    async def revert_cmd(event):
        await event.edit("🔄 `Restoring Original Profile...`")
        await client(functions.account.UpdateProfileRequest(first_name=ORIGINAL_NAME, about=ORIGINAL_BIO))
        await event.edit("✅ **Back to Normal!**")

    # --- 🔊 TEXT TO VOICE (TTS) ---
    @client.on(events.NewMessage(pattern=r"^[.! ]tts (.*)", outgoing=True))
    async def tts_handler(event):
        text = event.pattern_match.group(1)
        await event.edit("🎤 `Voice generating...`")
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text.replace(' ', '+')}&tl=hi&client=tw-ob"
        r = requests.get(url)
        with open("v.mp3", "wb") as f: f.write(r.content)
        await client.send_file(event.chat_id, "v.mp3", voice_note=True)
        await event.delete()
        os.remove("v.mp3")

    # --- 🤖 SMART AUTO-AI & MOOD ---
    @client.on(events.NewMessage(incoming=True))
    async def ai_auto_handler(event):
        global AUTO_AI, AFK_REASON
        if event.is_bot or not event.text: return
        
        # Mood Cheer-up
        if any(w in event.text.lower() for w in ["sad", "dukh", "rona", "alone"]):
            await event.reply(get_ai_response(event.text, "User is sad. Cheer them up in sweet Hinglish."))
            return

        if AUTO_AI and (event.is_private or f"@{me.username}" in event.text):
            async with event.client.action(event.chat_id, 'typing'):
                res = get_ai_response(event.text, f"You are {me.first_name}. Logical Hinglish chat.")
                await event.reply(res)

    # --- 🛡️ MODERATION & SPAM ---
    @client.on(events.NewMessage(pattern=r"^[.! ]antispam (on|off)", outgoing=True))
    async def spam_toggle(event):
        global SPAM_FILTER
        SPAM_FILTER = event.pattern_match.group(1) == "on"
        await event.edit(f"🛡️ **Spam Filter:** `{'ON' if SPAM_FILTER else 'OFF'}`")

    @client.on(events.NewMessage(incoming=True))
    async def spam_monitor(event):
        if SPAM_FILTER and event.is_group:
            if "http" in event.text or len(event.text) > 800:
                await event.delete()

    # --- 🎲 GAMES & FUN ---
    @client.on(events.NewMessage(pattern=r"^[.! ](dice|dart|slot|spin)", outgoing=True))
    async def fun_games(event):
        m = "🎲" if "dice" in event.text else "🎯" if "dart" in event.text else "🎰"
        await event.delete()
        await client.send_message(event.chat_id, file=types.InputMediaDice(m))

    @client.on(events.NewMessage(pattern=r"^[.! ]ai (.*)", outgoing=True))
    async def manual_ai(event):
        q = event.pattern_match.group(1)
        await event.edit("🤔 `Processing...`")
        await event.edit(f"🤖 **AI:** {get_ai_response(q)}")

    @client.on(events.NewMessage(pattern=r"^[.! ]autoai (on|off)", outgoing=True))
    async def ai_toggle(event):
        global AUTO_AI
        AUTO_AI = event.pattern_match.group(1) == "on"
        await event.edit(f"🤖 **Auto AI:** `{'ON' if AUTO_AI else 'OFF'}`")

    @client.on(events.NewMessage(pattern=r"^[.! ]ping", outgoing=True))
    async def ping_cmd(event):
        s = datetime.datetime.now()
        await event.edit("⚡")
        ms = (datetime.datetime.now() - s).microseconds / 1000
        await event.edit(f"🚀 **Pong!** `{ms}ms`")

    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())