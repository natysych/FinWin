from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Так, хочу почати 🎯", callback_data="start_yes")],
            [InlineKeyboardButton(text="Ні, повернутися ⬅️", callback_data="start_no")],
        ]
    )
    return keyboard

def continue_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Продовжити 👉", callback_data="cont_yes")],
            [InlineKeyboardButton(text="Повернутися ⬅️", callback_data="start_no")],
        ]
    )
    return keyboard
