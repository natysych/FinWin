from aiogram import Router, types, F
from aiohttp import web

from keyboards.pay_kb import payment_keyboard
from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

# --- ТАРИФИ ---
TARIFFS = {
    "pay_A": {
        "amount": 1500,
        "desc": "Повна оплата — 12 уроків",
        "folder": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    },
    "pay_B": {
        "amount": 800,
        "desc": "Оплата частинами — перші 6 уроків",
        "folder": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    },
    "pay_C": {
        "amount": 2000,
        "desc": "PRO доступ — повний курс + супровід",
        "folder": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    },
    "pay_D": {
        "amount": 3490,
        "desc": "MAX-програма — повний курс + бонуси",
        "folder": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
    },
}


# 🧾 Натискання на один із тарифів A/B/C/D
@router.callback_query(F.data.in_(TARIFFS.keys()))
async def start_payment(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tariff_id = callback.data  # "pay_A" / "pay_B" / ...

    tariff = TARIFFS[tariff_id]
    amount = tariff["amount"]
    description = tariff["desc"]

    # order_id — прив'язуємо платіж до користувача + тарифу
    order_id = f"{user_id}_{tariff_id}"

    # Генеруємо коректне посилання LiqPay (через services/liqpay.py)
    link = create_payment_link(
        amount=amount,
        description=description,
        order_id=order_id,
    )

    # Запам’ятовуємо, який тариф обрав юзер
    set_tariff_for_user(user_id, tariff_id)

    await callback.message.answer(
        f"💳 *Оплата тарифу:* _{description}_\n\n"
        f"Сума: *{amount} грн*\n\n"
        f"👉 Натисніть, щоб оплатити:\n{link}",
        parse_mode="Markdown",
    )
    await callback.answer()


# 📩 CALLBACK від LiqPay (поки мінімальний, просто приймаємо)
async def liqpay_callback(request: web.Request):
    data = await request.post()
    print("📩 LiqPay callback data:", data)
    return web.Response(text="OK")
