import os, sys, asyncio, datetime, requests, time, random, io, re
import pytz
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- CONFIGURATION (Quotes ke andar values bharein) ---
API_ID = "34769008" 
API_HASH = "98cc9d9d0750ba94abab2e60de1790a0"
SESSION_STRING = "1BVtsOKEBu3H0HfV72WmonKhUhefSprfgrakObI4WeQElpzNwcFouOgc80BDI3s9AUs4yasFI6eboqRQoZlJPiqZX1Ik7PeU_UXFAlVOizeT_t-LUocVJUcBrtm4QcXbBVO3UsI7ccnmVwRwiuxOyfWGjVG7V5nbANHk0PV-o80N4m7B3Cn1hkarqfZjMK_z68pnaaaUfhfppqPrXWKOEJn4TH5JRtQRirlWgFq4tN-ppnvXOdUJYouFLQP2KnDC8bZVpkzm2SYa1RQNO6LoCdFuPSYgJprJTwLoKR1bTpKy1xOZfgMNgGOTb48qsd7AjUDgVpmNDCDn92wUS7MnS1syJxDEy8fo="
OPENROUTER_KEY = "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" 
# ---------------------------------------------------

# Robust API_ID Handling
try:
    APP_ID = int(API_ID)
except:
    print("CRITICAL ERROR: API_ID is not a valid number!")
    APP_ID = 0

client = TelegramClient(StringSession(SESSION_STRING), APP_ID, API_HASH)
IST = pytz.timezone('Asia/Kolkata')
AI_MODEL = "google/gemini-2.0-flash-exp:free"

# STATE VARIABLES
AUTO_AI = False
AFK_REASON = None
SPAM_FILTER = False
ORIGINAL_NAME = ""
ORIGINAL_BIO = ""

def get_fancy(text):
    n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    f = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    return "".join([f[n.index(c)] if c in n else c for c in text])

def get_ai_response(prompt, system_p="You are a helpful assistant."):
    if not OPENROUTER_KEY or "VALUE" in OPENROUTER_KEY: return "Error: API Key Missing"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    data = {
        "model": AI_MODEL,
        "messages": [{"role": "system", "content": system_p}, {"role": "user", "content": prompt}]
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=15)
        resp = r.json()
        return resp['choices'][0]['message']['content'] if 'choices' in resp else "AI Error: Response not found"
    except: return "Connection Error"

async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot Active: {me.first_name}")

    # --- 📚 HELP MENU (SAB KUCH EK SAATH) ---
    @client.on(events.NewMessage(pattern=r"^[.! ]help", outgoing=True))
    async def help_cmd(event):
        h = f"👑 **{get_fancy('Supreme Legendary Bot')}**\n\n"
        h += "🎭 **PRO:** `.clone` | `.revert` | `.tts` [txt]\n"
        h += "🤖 **AI:** `.autoai on/off` | `.ai` | `.sum` | `.tr`\n"
        h += "🛡️ **MOD:** `.antispam on/off` | `.purge` | `.ban` | `.kick`\n"
        h += "😂 **FUN:** `.roast` | `.meme` | `.hack` | `.joke` | `.dare`\n"
        h += "🎲 **GAMES:** `.dice` | `.slot` | `.dart` | `.spin`\n"
        h += "🚀 **SYS:** `.ping` | `.alive` | `.id` | `.info`"
        await event.edit(h)

    # --- 🎭 PRO CLONE SYSTEM ---
    @client.on(events.NewMessage(pattern=r"^[.! ]clone", outgoing=True))
    async def clone_cmd(event):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("`Reply to someone!`")
        await event.edit("👤 `Cloning Profile...`")
        global ORIGINAL_NAME, ORIGINAL_BIO
        full_me = await client(functions.users.GetFullUserRequest(me.id))
        ORIGINAL_NAME, ORIGINAL_BIO = me.first_name, full_me.full_user.about or ""
        user = await client.get_entity(reply.sender_id)
        full_u = await client(functions.users.GetFullUserRequest(user.id))
        try:
            photos = await client.get_profile_photos(user.id)
            if photos:
                path = await client.download_media(photos[0])
                await client(functions.photos.UploadProfilePhotoRequest(await client.upload_file(path)))
            await client(functions.account.UpdateProfileRequest(first_name=user.first_name, about=full_u.full_user.about or ""))
            await event.edit(f"✅ **Identity Switched to {user.first_name}**")
        except Exception as e: await event.edit(f"Error: {e}")

    @client.on(events.NewMessage(pattern=r"^[.! ]revert", outgoing=True))
    async def revert_cmd(event):
        await event.edit("🔄 `Reverting...`")
        await client(functions.account.UpdateProfileRequest(first_name=ORIGINAL_NAME, about=ORIGINAL_BIO))
        await event.edit("✅ **Back to Normal!**")

    # --- 🤖 AI & MOOD ENGINE ---
    @client.on(events.NewMessage(pattern=r"^[.! ]autoai (on|off)", outgoing=True))
    async def ai_toggle(event):
        global AUTO_AI
        AUTO_AI = event.pattern_match.group(1) == "on"
        await event.edit(f"🤖 **Auto AI:** `{'ON' if AUTO_AI else 'OFF'}`")

    @client.on(events.NewMessage(incoming=True))
    async def pro_ai_handler(event):
        global AUTO_AI
        if event.is_bot or not event.text: return
        # Mood Detection (Hamara special touch)
        if any(w in event.text.lower() for w in ["sad", "rona", "breakup", "dukh"]):
            await event.reply(f"🌈 {get_ai_response(event.text, 'Cheer up user in 1 line sweet Hinglish.')}")
            return
        # Auto Chat Logic
        is_targeted = event.is_private or f"@{me.username}" in event.text or (event.is_reply and (await event.get_reply_message()).sender_id == me.id)
        if AUTO_AI and is_targeted:
            async with event.client.action(event.chat_id, 'typing'):
                await event.reply(get_ai_response(event.text, f"Act as {me.first_name}. Smart logical Hinglish chat."))

    # --- 🛡️ MODERATION & TOOLS ---
    @client.on(events.NewMessage(pattern=r"^[.! ]antispam (on|off)", outgoing=True))
    async def spam_toggle(event):
        global SPAM_FILTER
        SPAM_FILTER = event.pattern_match.group(1) == "on"
        await event.edit(f"🛡️ **Spam Filter:** `{'ON' if SPAM_FILTER else 'OFF'}`")

    @client.on(events.NewMessage(incoming=True))
    async def spam_handler(event):
        if SPAM_FILTER and event.is_group and ("http" in event.text or len(event.text) > 800):
            await event.delete()

    @client.on(events.NewMessage(pattern=r"^[.! ]purge", outgoing=True))
    async def purge_cmd(event):
        if not event.reply_to_msg_id: return await event.edit("`Reply to start.`")
        msgs = []
        async for msg in client.iter_messages(event.chat_id, min_id=event.reply_to_msg_id): msgs.append(msg)
        await client.delete_messages(event.chat_id, msgs)
        await event.edit(f"✅ **{len(msgs)} messages saaf!**"); await asyncio.sleep(2); await event.delete()

    # --- 😂 FUN & GAMES ---
    @client.on(events.NewMessage(pattern=r"^[.! ]roast", outgoing=True))
    async def roast_cmd(event):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("`Reply to roast someone!`")
        await event.edit("🔥 `Savage mode...`")
        res = get_ai_response(reply.text, "Brutal savage Hinglish roast. 2 lines.")
        await event.edit(f"💀 **{get_fancy('Roasted')}:**\n\n{res}")

    @client.on(events.NewMessage(pattern=r"^[.! ](dice|slot|dart|spin)", outgoing=True))
    async def game_cmd(event):
        em = "🎲" if "dice" in event.text else "🎯" if "dart" in event.text else "🎰"
        await event.delete(); await client.send_message(event.chat_id, file=types.InputMediaDice(em))

    @client.on(events.NewMessage(pattern=r"^[.! ]tts (.*)", outgoing=True))
    async def tts_cmd(event):
        txt = event.pattern_match.group(1); await event.edit("🔊 `Generating...`")
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={txt.replace(' ', '+')}&tl=hi&client=tw-ob"
        with open("v.mp3", "wb") as f: f.write(requests.get(url).content)
        await client.send_file(event.chat_id, "v.mp3", voice_note=True); await event.delete(); os.remove("v.mp3")

    # --- 🚀 SYSTEM ---
    @client.on(events.NewMessage(pattern=r"^[.! ]ping", outgoing=True))
    async def ping_cmd(event):
        s = datetime.datetime.now()
        await event.edit("⚡")
        ms = (datetime.datetime.now() - s).microseconds / 1000
        await event.edit(f"🚀 **Pong!** `{ms}ms`")

    @client.on(events.NewMessage(pattern=r"^[.! ]id", outgoing=True))
    async def id_cmd(event):
        r = await event.get_reply_message()
        await event.edit(f"🆔 **Chat:** `{event.chat_id}`\n🆔 **User:** `{r.sender_id if r else event.sender_id}`")

    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())