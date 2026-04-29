import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION ---
# Railway ke 'Variables' tab mein ye sab set karna hoga
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Agar variables nahi milte toh bot band ho jayega
if not API_ID or not API_HASH or not SESSION_STRING:
    print("Error: API_ID, API_HASH, ya SESSION_STRING missing hai!")
    sys.exit(1)

# Client Initialization using StringSession
client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)

async def main():
    print("Connecting to Telegram...")
    await client.start()
    me = await client.get_me()
    print(f"Userbot is Online! Logged in as: {me.first_name}")

    # 1. Ping Command (Network check karne ke liye)
    @client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
    async def ping(event):
        start = asyncio.get_event_loop().time()
        await event.edit("`Chasing the signal... 📡`")
        end = asyncio.get_event_loop().time()
        ms = round((end - start) * 1000, 2)
        await event.edit(f"**Pong!**\n`Speed: {ms}ms`\n`Host: Railway` 🚀")

    # 2. Say/Resend Command (Agar normal message send nahi ho raha)
    # Use: .say [aapka message]
    @client.on(events.NewMessage(pattern=r'\.say (.*)', outgoing=True))
    async def say(event):
        text = event.pattern_match.group(1)
        await event.delete()
        await client.send_message(event.chat_id, text)

    # 3. Help Command
    @client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
    async def help_cmd(event):
        help_text = (
            "**Railway Userbot active!**\n\n"
            "`.ping` - Network speed check karein\n"
            "`.say <msg>` - Network bypass karke message bhejein"
        )
        await event.edit(help_text)

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Kayi error aayi hai: {e}")