import os, sys, asyncio, datetime, requests, time, random, io
import pytz
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- CONFIGURATION (Apni details dhyan se bharein) ---
API_ID = 34769008 
API_HASH = "98cc9d9d0750ba94abab2e60de1790a0"
SESSION_STRING = "1BVtsOKEBu3H0HfV72WmonKhUhefSprfgrakObI4WeQElpzNwcFouOgc80BDI3s9AUs4yasFI6eboqRQoZlJPiqZX1Ik7PeU_UXFAlVOizeT_t-LUocVJUcBrtm4QcXbBVO3UsI7ccnmVwRwiuxOyfWGjVG7V5nbANHk0PV-o80N4m7B3Cn1hkarqfZjMK_z68pnaaaUfhfppqPrXWKOEJn4TH5JRtQRirlWgFq4tN-ppnvXOdUJYouFLQP2KnDC8bZVpkzm2SYa1RQNO6LoCdFuPSYgJprJTwLoKR1bTpKy1xOZfgMNgGOTb48qsd7AjUDgVpmNDCDn92wUS7MnS1syJxDEy8fo="
OPENROUTER_KEY = "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"
# --------------------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)
IST = pytz.timezone('Asia/Kolkata')
AI_MODEL = "google/gemini-2.0-flash-exp:free"

# GLOBALS
AFK_REASON = None

# Fancy font function (optimized)
def get_fancy(text):
    n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    f = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    return "".join([f[n.index(c)] if c in n else c for c in text])

# AI Response Function
def get_ai_response(prompt, user_name="User"):
    if not OPENROUTER_KEY or OPENROUTER_KEY == "VALUE": return "Key missing!"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    data = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": f"Short & fast response for {user_name}."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=7)
        return r.json()['choices'][0]['message']['content']
    except: return "AI currently offline."

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Userbot Started: {me.first_name}")

    # 1. HELP COMMAND (Now very fast)
    @client.on(events.NewMessage(pattern=r"^[.! ]help", outgoing=True))
    async def help_menu(event):
        h = f"📚 **{get_fancy('Master Userbot')}**\n\n"
        h += "🚀 `.ping` | `.alive` | `.afk` [reason]\n"
        h += "🎭 `.type` [text] | `.magic` | `.joke`\n"
        h += "👮 `.purge` | `.kick` | `.ban`\n"
        h += "🎨 `.love` | `.rose` | `.font` [text]\n"
        h += "🛠️ `.eval` [code] | `.say` [text]"
        await event.edit(h)

    # 2. PING & ALIVE (Ultra fast edit)
    @client.on(events.NewMessage(pattern=r"^[.! ]ping", outgoing=True))
    async def ping_cmd(event):
        start = datetime.datetime.now()
        await event.edit("⚡")
        ms = (datetime.datetime.now() - start).microseconds / 1000
        await event.edit(f"🚀 **Pong!** `{ms}ms`")

    @client.on(events.NewMessage(pattern=r"^[.! ]alive", outgoing=True))
    async def alive_cmd(event):
        await event.edit(f"✅ **{get_fancy('Userbot is Active')}**\n👤 **Owner:** `{me.first_name}`")

    # 3. AFK & AI REPLIES
    @client.on(events.NewMessage(pattern=r"^[.! ]afk", outgoing=True))
    async def set_afk(event):
        global AFK_REASON
        AFK_REASON = event.text.split(None, 1)[1] if " " in event.text else "Busy"
        await event.edit(f"💤 **AFK Enabled:** `{AFK_REASON}`")

    @client.on(events.NewMessage(incoming=True))
    async def auto_reply(event):
        global AFK_REASON
        if AFK_REASON and event.is_private:
            async with event.client.action(event.chat_id, 'typing'):
                res = get_ai_response(event.text, me.first_name)
                await event.reply(f"🤖 **AI Mode:**\n{res}")

    # 4. FUN & UTILS
    @client.on(events.NewMessage(pattern=r"^[.! ](type|magic|love|rose|joke)", outgoing=True))
    async def fun_handler(event):
        cmd = event.pattern_match.group(1).lower()
        if cmd == "type":
            t = event.text.split(None, 1)[1] if " " in event.text else "Typing..."
            curr = ""
            for char in t:
                curr += char
                await event.edit(f"`{curr}|`")
                await asyncio.sleep(0.05)
        elif cmd == "magic":
            for m in ["🎩","🪄","✨","🐰"]:
                await event.edit(m); await asyncio.sleep(0.3)
            await event.edit("✨ **Ta-Da! Magic!**")
        elif cmd == "love":
            await event.edit("❤️ **I Love You!**")
        elif cmd == "rose":
            await event.edit("🌹 **A rose for you!**")
        elif cmd == "joke":
            j = requests.get("https://official-joke-api.appspot.com/random_joke").json()
            await event.edit(f"😂 **Joke:**\n{j['setup']}\n\n*— {j['punchline']}*")

    # 5. ADMIN TOOLS
    @client.on(events.NewMessage(pattern=r"^[.! ]purge", outgoing=True))
    async def purge_cmd(event):
        if not event.reply_to_msg_id:
            return await event.edit("`Reply to a message to start purging.`")
        msgs = []
        async for msg in client.iter_messages(event.chat_id, min_id=event.reply_to_msg_id):
            msgs.append(msg)
        await client.delete_messages(event.chat_id, msgs)
        await event.edit(f"✅ **Purged {len(msgs)} messages!**")
        await asyncio.sleep(2); await event.delete()

    # 6. EVAL (Power User)
    @client.on(events.NewMessage(pattern=r"^[.! ]eval (.*)", outgoing=True))
    async def eval_cmd(event):
        code = event.pattern_match.group(1)
        await event.edit("`Running...` ⚡")
        try:
            # Simple eval for single lines
            res = eval(code)
            if asyncio.iscoroutine(res): res = await res
            await event.edit(f"**Code:**\n`{code}`\n\n**Output:**\n`{res}`")
        except Exception as e:
            await event.edit(f"**Error:**\n`{e}`")

    await client.run_until_disconnected()

print("Initialising...")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())