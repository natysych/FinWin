# services/reminders.py

import asyncio
from aiogram import Bot
from config import TOKEN

from services.storage import (
    get_unsubscribed_users,
    get_all_user_ids,
    get_user_state
)

REMINDER_TEXT = (
    "👋 Ми все ще чекаємо на вас у FinanceForTeens!\n"
    "💛 Поверніться, оберіть тариф та почніть шлях до фінансової свободи 💛"
)


async def reminders_loop(bot: Bot):
    """
    2 рази на добу нагадує тим, хто натиснув «Ні» (unsubscribed).
    """
    while True:
        try:
            unsubscribed = get_unsubscribed_users()

            for user_id in unsubscribed:
                await bot.send_message(user_id, REMINDER_TEXT)

            # 12 годин пауза
            await asyncio.sleep(60 * 60 * 12)

        except Exception as e:
            print("❌ REMINDER ERROR:", e)
            await asyncio.sleep(60)  # пауза 1 хв, щоб не падати
