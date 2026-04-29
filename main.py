import os, sys, asyncio, datetime, requests, time, random, io
import pytz
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- CONFIGURATION (Directly put your values here) ---

API_ID = 34769008  # Example: 1234567 (Isme quotes mat lagana)
API_HASH = "98cc9d9d0750ba94abab2e60de1790a0"  # Example: "abc123def456..."
SESSION_STRING = "1BVtsOKEBu3H0HfV72WmonKhUhefSprfgrakObI4WeQElpzNwcFouOgc80BDI3s9AUs4yasFI6eboqRQoZlJPiqZX1Ik7PeU_UXFAlVOizeT_t-LUocVJUcBrtm4QcXbBVO3UsI7ccnmVwRwiuxOyfWGjVG7V5nbANHk0PV-o80N4m7B3Cn1hkarqfZjMK_z68pnaaaUfhfppqPrXWKOEJn4TH5JRtQRirlWgFq4tN-ppnvXOdUJYouFLQP2KnDC8bZVpkzm2SYa1RQNO6LoCdFuPSYgJprJTwLoKR1bTpKy1xOZfgMNgGOTb48qsd7AjUDgVpmNDCDn92wUS7MnS1syJxDEy8fo="  # Aapka Telethon Session String
OPENROUTER_KEY = "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"  # OpenRouter API Key

# ---------------------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
IST = pytz.timezone('Asia/Kolkata')
AI_MODEL = "google/gemini-2.0-flash-exp:free"

# --- PREMIUM EMOJI IDs ---
EMOJI_MAGIC = 5431443046535175653 
EMOJI_ALIVE = 5442978931139314811 
EMOJI_HELP = 5463105436695574510  
EMOJI_HEART = 5429393664323249089 

# --- Rest of the code stays the same ---
# (Pura code jo maine pehle diya tha, baaki sab waisa hi rahega)
 

# --- Rest of the code stays the same ---
# (Pura code jo maine pehle diya tha, baaki sab waisa hi rahega)


# --- GLOBALS ---
AFK_REASON = None

# --- FANCY FONTS ---
NORMAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
FANCY = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
def get_fancy(text):
    return "".join([FANCY[NORMAL.index(c)] if c in NORMAL else c for c in text])

# --- AI FUNCTION (OPENROUTER) ---
def get_ai_response(prompt, user_name="User"):
    if not OPENROUTER_KEY: return "AI Key missing in Railway variables!"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    
    full_prompt = f"You are a smart AI assistant for {user_name}. Keep your replies short, natural, and in Hinglish. Current Status: AFK."
    
    data = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except: return "I'm currently busy. Will talk to you later!"

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Master Bot Started as {me.first_name}")

    # 1. HELP MENU
    @client.on(events.NewMessage(pattern=r"^[.! ]help", outgoing=True))
    async def help_menu(event):
        help_text = f"""
<{types.MessageEntityCustomEmoji(offset=0, length=2, document_id=EMOJI_HELP)}> **{get_fancy('Master Userbot Help')}**

🚀 **NETWORK**
`.ping` | `.speedtest` | `.alive` | `.say [txt]`

🤖 **AI & AUTO**
`.afk [reason]` | `.font [txt]` | `AI-Reply`

👮 **ADMIN**
`.ban` | `.mute` | `.kick` | `.purge` (Reply)

🎭 **MAGIC & FUN**
`.type [txt]` | `.magic` | `.bomb` | `.joke` | `.roast`

🎨 **ART**
`.love` | `.rose` | `.heart` | `.gun`

🛠️ **DEV TOOLS**
`.eval [code]` | `.p [emoji_id]`

_Prefix: . or ! both work_
"""
        await event.edit(help_text)

    # 2. PREMIUM ALIVE & PING
    @client.on(events.NewMessage(pattern=r"^[.! ]alive", outgoing=True))
    async def alive_cmd(event):
        msg = f"<{types.MessageEntityCustomEmoji(offset=0, length=1, document_id=EMOJI_ALIVE)}> {get_fancy('Userbot is Online!')}\n\n"
        msg += f"👤 **Owner:** `{me.first_name}`\n⚡ **Status:** `Smooth` | **AI:** `Ready`"
        await event.edit(msg)

    @client.on(events.NewMessage(pattern=r"^[.! ]ping", outgoing=True))
    async def ping_cmd(event):
        start = datetime.datetime.now()
        await event.edit("⚡")
        end = datetime.datetime.now()
        ms = (end - start).microseconds / 1000
        await event.edit(f"<{types.MessageEntityCustomEmoji(offset=0, length=1, document_id=EMOJI_MAGIC)}> **Pong!** `{ms}ms`")

    # 3. MAGIC EFFECTS
    @client.on(events.NewMessage(pattern=r"^[.! ](type|magic|bomb|loading)", outgoing=True))
    async def magic_handler(event):
        cmd = event.pattern_match.group(1).lower()
        if cmd == "type":
            text = event.text.split(None, 1)[1] if " " in event.text else "Hello!"
            t = ""
            for c in text:
                t += c
                await event.edit(f"`{t}|`")
                await asyncio.sleep(0.1)
        elif cmd == "magic":
            for f in ["🃏","🪄","✨","🎩","🐰"]:
                await event.edit(f); await asyncio.sleep(0.4)
            await event.edit(f"<{types.MessageEntityCustomEmoji(offset=0, length=2, document_id=EMOJI_MAGIC)}> **Magic Done!**")
        elif cmd == "bomb":
            for n in ["5️⃣","4️⃣","3️⃣","2️⃣","1️⃣","💥"]:
                await event.edit(n); await asyncio.sleep(0.5)
            await event.delete()

    # 4. AI AFK HANDLER
    @client.on(events.NewMessage(incoming=True))
    async def ai_afk(event):
        global AFK_REASON
        if AFK_REASON and not event.is_group and not event.is_bot:
            async with event.client.action(event.chat_id, 'typing'):
                res = get_ai_response(event.text, me.first_name)
                await event.reply(f"🤖 **ᴀɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ:**\n{res}")

    # 5. CORE TOOLS (AFK, EVAL, SAY, ART)
    @client.on(events.NewMessage(pattern=r"^[.! ](afk|eval|say|love|rose)", outgoing=True))
    async def core_handler(event):
        cmd = event.pattern_match.group(1).lower()
        if cmd == "afk":
            global AFK_REASON
            AFK_REASON = event.text.split(None, 1)[1] if " " in event.text else "Away"
            await event.edit(get_fancy(f"AFK Enabled: {AFK_REASON}"))
        elif cmd == "eval":
            code = event.text.split(None, 1)[1]
            try:
                result = await eval(code)
                await event.edit(f"**Code:** `{code}`\n**Result:** `{result}`")
            except Exception as e: await event.edit(f"**Error:** `{e}`")
        elif cmd == "love":
            await event.edit(f"<{types.MessageEntityCustomEmoji(offset=0, length=1, document_id=EMOJI_HEART)}> {get_fancy('I Love You')}")
        elif cmd == "say":
            msg = event.text.split(None, 1)[1]
            await event.delete(); await client.send_message(event.chat_id, msg)

    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())