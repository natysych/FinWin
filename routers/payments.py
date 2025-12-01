from aiogram import Router, types
from aiogram.types import CallbackQuery
import time
from aiohttp import web
import base64
import json

from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user


router = Router()

# ---- ТАРИФИ ----
TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн"},
    "B": {"amount": 800, "name": "Частинами — 800 грн (6 уроків)"},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн"},
    "D": {"amount": 3490, "name": "MAX — 3490 грн"},
}


# -----------------------------------------------------------
# 👉 ОБРОБКА ВИБОРУ ТАРИФУ (створюємо зовнішній LiqPay-лінк)
# -----------------------------------------------------------
@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # Унікальний order_id
    # 👇 Дуже важливо: user_id всередині!
    order_id = f"{callback.from_user.id}_{int(time.time())}_{tariff}"

    # Зберегти тариф у локальну базу
    set_tariff_for_user(callback.from_user.id, tariff)

    # Створити лінк LiqPay
    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id
    )

    # Відповідь користувачу
    await callback.message.answer(
        f"💎 *Тариф {tariff} — {info['name']}*\n\n"
        f"🔗 Для оплати перейдіть за посиланням:\n{link}",
        parse_mode="Markdown"
    )

    await callback.answer()


# -----------------------------------------------------------
# 👉 CALLBACK LiqPay → запуск логіки оплати
# -----------------------------------------------------------
async def liqpay_callback(request: web.Request):
    """
    LiqPay надсилає POST { data, signature }
    Ми перевіряємо статус і оновлюємо користувача.
    """
    try:
        payload = await request.post()

        lp_data = payload.get("data")
        lp_sign = payload.get("signature")

        print("🔥 CALLBACK RECEIVED:", payload)

        if not lp_data:
            return web.Response(text="no data")

        decoded = json.loads(base64.b64decode(lp_data).decode())

        order_id = decoded.get("order_id")
        status = decoded.get("status")

        print("🔥 ORDER:", order_id, "| STATUS:", status)

        # статуси що вважаємо успішними
        if status in ("success", "sandbox"):
            try:
                # order_id = "userId_timestamp_tariff"
                user_id, ts, tariff = order_id.split("_")
                set_tariff_for_user(int(user_id), tariff)
                print("✅ Tariff saved for user:", user_id, tariff)

            except Exception as e:
                print("❌ Failed to parse order_id:", e)

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
