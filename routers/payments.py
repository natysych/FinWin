from aiogram import Router, types, F
from services.liqpay import create_payment

router = Router()

@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]

    amount = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490
    }[tariff]

    pay_link = create_payment(
        amount=amount,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=f"{tariff}_{callback.from_user.id}"
    )

    await callback.message.answer(
        f"💳 Натисніть, щоб сплатити тариф {tariff}:\n{pay_link}"
    )
