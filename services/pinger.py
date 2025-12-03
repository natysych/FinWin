import aiohttp
import asyncio
import os

PING_URL = os.getenv("PING_URL")


async def keep_alive():
    """Пінгує Railway кожні 4 хвилини, щоб контейнер не засинав."""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PING_URL) as resp:
                    print("🔄 Ping Railway:", resp.status)
        except Exception as e:
            print("❌ Ping error:", e)

        await asyncio.sleep(240)  # 4 minutes
