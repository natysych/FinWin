import time
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.liqpay import create_payment_link
from services.storage import set_user_tariff

router = Router()

# Твої посилання на курси
COURSE_LINK_A = "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV"
COURSE_LINK_B = "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ"
COURSE_LINK_C = "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6"
COURSE_LINK_D = "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ"

TARIFFS = {
    "A": {
        "title": "Тариф A — Повний курс",
        "amount": 1500,
        "description": "FinanceForTeens: Тариф A — Повний курс",
        "course_link": COURSE_LINK_A,
    },
    "B": {
        "title": "Тариф B — Старт (6 уроків)",
        "amount": 800,
        "description": "FinanceForTeens: Тариф B — Старт (6 уроків)",
        "course_link": COURSE_LINK_B,
    },
    "C": {
        "title": "Тариф C — PRO + куратор",
        "amount": 2000,
        "description": "FinanceForTeens: Тариф C — PRO + куратор",
        "course_link": COURSE_LINK_C,
    },
    "D": {
        "title": "Тариф D — MAX 6 міс + бонуси",
        "amount": 3490,
        "description": "FinanceForTeens: Тариф D — MAX 6 міс + бонуси",
        "course_link": COURSE_LINK_D,
    },
}


@router.callback_query(lambda c: c.data in ("pay_A", "pay_B", "pay_C", "pay_D"))
async def handle_tariff_choose(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tariff_code = callback.data.split("_")[1]  # 'A' / 'B' / 'C' / 'D'
    tariff = TARIFFS[tariff_code]

    # Запам’ятовуємо тариф користувача (для видачі правильного курсу після анкети)
    set_user_tariff(user_id, tariff_code)

    # Унікальний order_id
    order_id = f"{tariff_code}_{user_id}_{int(time.time())}"

    pay_url = create_payment_link(
        amount=tariff["amount"],
        description=tariff["description"],
        order_id=order_id,
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Перейти до оплати", url=pay_url
                )
            ]
        ]
    )

    text = (
        f"✅ Ви обрали *{tariff['title']}*.\n"
        f"Сума до оплати: *{tariff['amount']} грн*.\n\n"
        "Натисніть кнопку нижче, щоб перейти на сторінку оплати LiqPay 👇"
    )

    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
