from aiogram import Router, types, F
from services.liqpay import create_payment
from services.storage import set_tariff_for_user, set_unsubscribed

router = Router()

@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]  # "A" / "B" / "C" / "D"

    amount_map = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490,
    }

    titles = {
        "A": "Повний курс (12 уроків) 💎",
        "B": "Перші 6 уроків 📘",
        "C": "PRO доступ + ментор 🎯",
        "D": "MAX програмa + бонуси 🚀",
    }

    amount = amount_map[tariff]
    user_id = callback.from_user.id

    # save tariff
    set_tariff_for_user(user_id, tariff)
    set_unsubscribed(user_id, False)

    order_id = f"{tariff}_{user_id}"

    link = create_payment(
        amount=amount,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=order_id,
    )

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="💳 Перейти до оплати", url=link)]
        ]
    )

    await callback.message.answer(
        f"Оберіть спосіб оплати для тарифу: *{titles[tariff]}*",
        reply_markup=kb,
        parse_mode="Markdown"
    )
