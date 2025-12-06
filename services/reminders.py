import asyncio
from aiogram import Bot

from services.storage import (
    get_unsubscribed_user_ids,
    get_user_state,
)

REMINDER_TEXT = (
    "👋 Ми все ще чекаємо на вас у FinanceForTeens!\n"
    "💛 Поверніться, оберіть тариф та почніть шлях до фінансової свободи 💛"
)


async def send_reminder(bot: Bot, user_id: int):
    try:
        await bot.send_message(user_id, REMINDER_TEXT)
    except Exception as e:
        print(f"⚠ Не вдалося надіслати нагадування {user_id}: {e}")


async def reminders_loop(bot: Bot):
    print("⏰ Reminder loop started")

    while True:
        try:
            unsubscribed = get_unsubscribed_user_ids()
            print("🔍 Unsubscribed users:", unsubscribed)

            for user_id in unsubscribed:
                state = get_user_state(user_id)
                if state != "unsubscribed":
                    continue

                await send_reminder(bot, user_id)

            # чекати 12 годин
            await asyncio.sleep(60 * 60 * 12)

        except Exception as e:
            print("❌ Reminder loop error:", e)
            await asyncio.sleep(60)
