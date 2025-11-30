from aiogram import Router, types
from keyboards.pay_kb import payment_keyboard
from services.storage import set_tariff_for_user
from liqpay import create_payment

router = Router()


TARIFF_NAMES = {
    "A": "Повна оплата — 12 уроків",
    "B": "Оплата частинами — 6 уроків",
    "C": "PRO доступ — курс + ментор",
    "D": "MAX програма — 6 місяців + бонуси"
}


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

    # Зберігаємо тариф
    set_tariff_for_user(callback.from_user.id, tariff)

    # Суми тарифа
    amounts = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490
    }

    amount = amounts.get(tariff, 0)
    tariff_name = TARIFF_NAMES.get(tariff, "Обраний тариф")

    order_id = f"{callback.from_user.id}_{tariff}"

    payment_url = create_payment(
        amount=amount,
        description=f"{tariff_name} ({tariff})",
        order_id=order_id
    )

    await callback.message.answer(
        f"💳 *{tariff_name}*\n\n"
        f"Натисніть, щоб оплатити тариф **{tariff}**:\n{payment_url}",
        parse_mode="Markdown"
    )
    await callback.answer()
