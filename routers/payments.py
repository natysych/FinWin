from aiogram import Router, types
from keyboards.pay_kb import payment_keyboard
from services.storage import set_tariff_for_user
from liqpay import create_payment

router = Router()


@router.callback_query(lambda c: c.data == "cont_yes")
async def choose_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 У нас є декілька форматів, оберіть той, що підходить вам найбільше.\n"
        "Після оплати ми попросимо заповнити анкету та надішлемо доступ до курсу.",
        reply_markup=payment_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1].upper()

    set_tariff_for_user(callback.from_user.id, tariff)

    amounts = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490
    }

    amount = amounts.get(tariff, 0)
    order_id = f"{callback.from_user.id}_{tariff}"

    payment_url = create_payment(
        amount=amount,
        description=f"FinanceForTeens — тариф {tariff}",
        order_id=order_id
    )

    await callback.message.answer(
        f"💳 Натисніть кнопку, щоб оплатити тариф {tariff}:\n{payment_url}"
    )
    await callback.answer()
