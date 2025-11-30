from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Так, хочу далі!", callback_data="start_yes")],
        [InlineKeyboardButton(text="❌ Ні, відписатись", callback_data="start_no")]
    ])

def continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 Так, продовжимо!", callback_data="cont_yes")],
        [InlineKeyboardButton(text="❌ Відписатись", callback_data="start_no")]
    ])
