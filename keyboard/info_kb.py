from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def info_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Публічна оферта",
                    url="https://natysych.github.io/FINWIN/offer.pdf"
                )
            ]
        ]
    )
