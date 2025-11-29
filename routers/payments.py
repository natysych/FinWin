from aiogram import Router, types, F
from services.liqpay import create_payment
from services.storage import set_tariff_for_user, set_unsubscribed

router = Router()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]  # A / B / C / D

    amount = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490,
    }[tariff]

    user_id = callback.from_user.id
    # Запам’ятовуємо, який тариф оплатив користувач
    set_tariff_for_user(user_id, tariff)
    # Він вже не в статусі unsubscribed
    set_unsubscribed(user_id, False)

    pay_link = create_payment(
        amount=amount,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=f"{tariff}_{user_id}",
    )

    await callback.message.answer(
        f"💳 Натисніть, щоб сплатити тариф {tariff}:\n{pay_link}"
    )
