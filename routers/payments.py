from aiogram import Router, types
from aiogram.types import CallbackQuery
import time

from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн"},
    "B": {"amount": 800, "name": "Частинами — 800 грн"},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн"},
    "D": {"amount": 3490, "name": "MAX-програма — 3490 грн"},
}


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # Унікальний order_id
    order_id = f"{int(time.time())}_{tariff}"

    # Зберегти тариф
    set_tariff_for_user(callback.from_user.id, tariff)

    # Створити посилання оплат
    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id
    )

    await callback.message.answer(
        f"💎 Тариф {tariff} — {info['name']}\n\n"
        f"Перейдіть за посиланням для оплати:\n"
        f"{link}"
    )
    await callback.answer()
