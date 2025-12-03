# file: keyboards/pay_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="A) Повна оплата — 1500 грн",
                    callback_data="pay_A",
                )
            ],
            [
                InlineKeyboardButton(
                    text="B) Оплата частинами — 800 грн",
                    callback_data="pay_B",
                )
            ],
            [
                InlineKeyboardButton(
                    text="C) PRO доступ — 2000 грн",
                    callback_data="pay_C",
                )
            ],
            [
                InlineKeyboardButton(
                    text="D) MAX-програма — 3490 грн",
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
