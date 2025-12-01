from aiogram import Router, types
from services.storage import set_tariff_for_user
from services.liqpay import create_payment_link

router = Router()


# --- ТАРИФИ ---
TARIFFS = {
    "A": {
        "amount": 1500,
        "title": "Повна оплата — 12 уроків"
    },
    "B": {
        "amount": 800,
        "title": "Частинами — 6 уроків"
    },
    "C": {
        "amount": 2000,
        "title": "PRO — повний курс + 1 місяць менторства"
    },
    "D": {
        "amount": 3490,
        "title": "MAX — 6 міс програма + бонуси + ком'юніті"
    }
}


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(call: types.CallbackQuery):
    tariff_code = call.data.split("_")[1]

    if tariff_code not in TARIFFS:
        await call.message.answer("❗ Помилка: тариф не знайдено.")
        return

    # Зберігаємо тариф за користувачем
    user_id = call.from_user.id
    set_tariff_for_user(user_id, tariff_code)

    tariff = TARIFFS[tariff_code]

    # Створюємо order_id (унікальний)
    order_id = f"{user_id}_{tariff_code}"

    # Створюємо посилання LiqPay
    link = create_payment_link(
        amount=tariff["amount"],
        description=tariff["title"],
        order_id=order_id
    )

    await call.message.answer(
        f"💳 *{tariff['title']}*\n\n"
        "Натисніть кнопку нижче, щоб здійснити оплату ⬇️",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="👉 Перейти до оплати",
                        url=link
                    )
                ]
            ]
        )
    )


# --- CALLBACK ВІД LIQPAY ---
# (обробляється Railway через liqpay_callback.py)
# тут ми лише повторно не ловимо його, щоби уникнути дублювання
