from aiogram import Router, types, F
from services.liqpay import create_payment
from services.storage import set_tariff_for_user, set_unsubscribed

router = Router()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    """
    Користувач обрав тариф A/B/C/D.
    Створюємо order_id, генеруємо LiqPay-лінк,
    показуємо кнопку "Перейти до оплати", без сирого посилання в тексті.
    """
    tariff = callback.data.split("_")[1]  # "A" / "B" / "C" / "D"

    amount_map = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490,
    }

    amount = amount_map[tariff]
    user_id = callback.from_user.id

    # Запам’ятовуємо тариф користувача
    set_tariff_for_user(user_id, tariff)
    set_unsubscribed(user_id, False)

    order_id = f"{tariff}_{user_id}"

    pay_link = create_payment(
        amount=amount,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=order_id,
    )

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Перейти до оплати в LiqPay 💳",
                    url=pay_link,
                )
            ]
        ]
    )

    await callback.message.answer(
        f"Щоб оплатити тариф {tariff}, натисніть кнопку нижче 👇",
        reply_markup=keyboard,
    )
