import aiohttp
from config import OPENROUTER_KEY

async def ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    async with aiohttp.ClientSession() as s:
        async with s.post(url,
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages":[{"role":"user","content":prompt}]
            }
        ) as r:
            res = await r.json()
            return res["choices"][0]["message"]["content"]