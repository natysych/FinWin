from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.storage import set_tariff_for_user
from liqpay import create_payment

router = Router()

TARIFF_NAMES = {
    "A": "Повна оплата — 12 уроків",
    "B": "Частинами — 6 уроків",
    "C": "PRO — курс + ментор",
    "D": "MAX — 6 місяців",
}

AMOUNTS = {
    "A": 1500,
    "B": 800,
    "C": 2000,
    "D": 3490,
}


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1].upper()
    set_tariff_for_user(callback.from_user.id, tariff)

    amount = AMOUNTS[tariff]
    order_id = f"{callback.from_user.id}_{tariff}"

    payment_url = create_payment(
        amount=amount,
        description=TARIFF_NAMES[tariff],
        order_id=order_id,
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатити", url=payment_url)]
        ]
    )

    await callback.message.answer(
        f"💳 *{TARIFF_NAMES[tariff]}*\nНатисніть кнопку, щоб перейти до оплати.",
        parse_mode="Markdown",
        reply_markup=markup
    )
    await callback.answer()
