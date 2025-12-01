from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot
from config import TOKEN

bot = Bot(token=TOKEN)

await bot.send_message(
    user_id,
    "🎉 *Оплату отримано!*\n\n"
    "Будь ласка, заповніть коротку анкету, щоб ми могли створити ще кращий продукт для вас 💛\n\n"
    f"📝 Анкета: {SURVEY_LINK}\n\n"
    "Коли заповните — натисніть *Готово*.",
    parse_mode="Markdown",
    reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Готово")]],
        resize_keyboard=True
    )
)

await bot.session.close()
