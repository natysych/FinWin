from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Так", callback_data="start_yes")],
            [InlineKeyboardButton(text="Ні/unsubscribe", callback_data="unsubscribe")],
        ]
    )

def continue_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Так", callback_data="cont_yes")],
            [InlineKeyboardButton(text="Ні/unsubscribe", callback_data="unsubscribe")],
        ]
    )
