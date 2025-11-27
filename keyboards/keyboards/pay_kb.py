from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def payment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 A) 1500 грн", callback_data="pay_A")],
        [InlineKeyboardButton(text="💳 B) 800 грн", callback_data="pay_B")],
        [InlineKeyboardButton(text="🔥 C) 2000 грн", callback_data="pay_C")],
        [InlineKeyboardButton(text="👑 D) 3490 грн", callback_data="pay_D")],
    ])
