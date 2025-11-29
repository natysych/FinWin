import asyncio
from aiogram import Bot
from services.storage import get_unsubscribed_user_ids

REMINDER_TEXT = (
    "👋 Ми все ще чекаємо на вас у FinanceForTeens!\n"
    "💛Поверніться, оберіть тариф та почніть шлях до фінансової свободи 💛"
)


async def reminders_loop(bot: Bot):
    while True:
        user_ids = get_unsubscribed_user_ids()
        for uid in user_ids:
            try:
                await bot.send_message(uid, REMINDER_TEXT)
            except Exception:
                pass
        # Раз на 12 годин → 2 нагадування на добу
        await asyncio.sleep(60 * 60 * 12)
