from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def payment_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 Тариф A — 1500 грн", callback_data="pay_A")],
            [InlineKeyboardButton(text="💳 Тариф B — 800 грн", callback_data="pay_B")],
            [InlineKeyboardButton(text="🔥 Тариф C — 2000 грн", callback_data="pay_C")],
            [InlineKeyboardButton(text="👑 Тариф D — 3490 грн", callback_data="pay_D")],

            [InlineKeyboardButton(text="📄 Публічна оферта", callback_data="offer")]
        ]
    )
