from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

AMOUNTS = {
    "A": 1500,
    "B": 800,
    "C": 2000,
    "D": 3490
}


@router.callback_query(lambda c: c.data == "cont_yes")
async def choose_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 Оберіть формат навчання, що підходить вам найбільше.\n"
        "Після оплати ми попросимо заповнити анкету та надішлемо доступ до курсу."
    )

    await callback.message.answer(
        "Оберіть тариф:",
        reply_markup=payment_keyboard()
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1].upper()

    # Зберігаємо тариф
    set_tariff_for_user(callback.from_user.id, tariff)

    amount = AMOUNTS.get(tariff)
    order_id = f"{callback.from_user.id}_{tariff}"

    payment_url = create_payment(
        amount=amount,
        description=f"{TARIFF_NAMES[tariff]} ({tariff})",
        order_id=order_id
    )

    # КНОПКА З ЗОВНІШНІМ ПОСИЛАННЯМ
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатити", url=payment_url)]
        ]
    )

    await callback.message.answer(
        f"💳 *{TARIFF_NAMES[tariff]}*\n\n"
        f"Натисніть кнопку нижче, щоб перейти до оплати.",
        parse_mode="Markdown",
        reply_markup=markup
    )

    await callback.answer()
