import aiohttp
from config import OPENROUTER_KEY
from core.memory import build_context

async def ai(uid, prompt):
    context = build_context(uid)

    async with aiohttp.ClientSession() as s:
        async with s.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {"role":"system","content":"You are smart Hinglish AI"},
                    {"role":"user","content": context + "\n" + prompt}
                ]
            }
        ) as r:
            res = await r.json()
            return res["choices"][0]["message"]["content"]