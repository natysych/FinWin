from aiogram import Router, types
from keyboards.pay_kb import payment_keyboard
from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

TARIFFS = {
    "A": 1500,
    "B": 800,
    "C": 2000,
    "D": 3490,
}

DESCRIPTIONS = {
    "A": "Повний курс (12 уроків)",
    "B": "6 уроків (перша частина)",
    "C": "PRO доступ (12 уроків + ментор)",
    "D": "MAX програма (6 місяців)",
}


@router.callback_query(lambda c: c.data == "show_payments")
async def show_payments(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 У нас є декілька форматів, оберіть той, що підходить вам найбільше.\n"
        "Після оплати ми попросимо заповнити анкету та надішлемо доступ до курсу.",
        reply_markup=payment_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def choose_tariff(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]

    amount = TARIFFS[tariff]
    description = DESCRIPTIONS[tariff]

    order_id = f"{callback.from_user.id}_{tariff}"

    pay_link = create_payment_link(amount, description, order_id)

    await callback.message.answer(
        f"💳 Натисніть, щоб оплатити тариф {tariff}:\n{pay_link}"
    )
