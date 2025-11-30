from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_type_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура з вибором тарифу + публічна оферта.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Тариф A — Повний курс (1500 грн)",
                    callback_data="pay_A",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Тариф B — Старт (перші 6 уроків, 800 грн)",
                    callback_data="pay_B",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔥 Тариф C — PRO + куратор (2000 грн)",
                    callback_data="pay_C",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 Тариф D — MAX 6 міс + бонуси (3490 грн)",
                    callback_data="pay_D",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 Публічна оферта",
                    callback_data="offer",
                )
            ],
        ]
    )
