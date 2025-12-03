# file: services/reminders.py
import asyncio
from datetime import datetime, date
from aiogram import Bot

from services.storage import get_unsubscribed_user_ids


async def reminders_loop(bot: Bot):
    """
    Двічі на день (10:00 і 19:00) нагадуємо тим, хто відписався.
    """
    last_morning: date | None = None
    last_evening: date | None = None

    while True:
        now = datetime.now()
        today = now.date()
        hour = now.hour
        minute = now.minute

        # Ранкове нагадування
        if hour == 10 and minute == 0 and last_morning != today:
            user_ids = get_unsubscribed_user_ids()
            for uid in user_ids:
                try:
                    await bot.send_message(
                        uid,
                        "👋 Ми все ще чекаємо на вас у FinanceForTeens!\n"
                        "💛Поверніться, оберіть тариф та почніть шлях до фінансової свободи 💛"
                    )
                except Exception as e:
                    print("Reminder morning error for", uid, e)
            last_morning = today

        # Вечірнє нагадування
        if hour == 19 and minute == 0 and last_evening != today:
            user_ids = get_unsubscribed_user_ids()
            for uid in user_ids:
                try:
                    await bot.send_message(
                        uid,
                        "👋 Ми все ще чекаємо на вас у FinanceForTeens!\n"
                        "💛Поверніться, оберіть тариф та почніть шлях до фінансової свободи 💛"
                    )
                except Exception as e:
                    print("Reminder evening error for", uid, e)
            last_evening = today

        await asyncio.sleep(30)
