from aiogram import Router, types
from aiogram.types import CallbackQuery
import time
from aiohttp import web

from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

# --- Тарифи ---
TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн"},
    "B": {"amount": 800,  "name": "Частинами — 800 грн"},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн"},
    "D": {"amount": 3490, "name": "MAX-програма — 3490 грн"},
}


# ================================
#  Генерація посилання на оплату
# ================================
@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # Унікальний order_id: userID_tariff_timestamp
    order_id = f"{callback.from_user.id}_{tariff}_{int(time.time())}"

    # Зберегти тариф одразу
    set_tariff_for_user(callback.from_user.id, tariff)

    # Генерувати посилання LiqPay
    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id
    )

    await callback.message.answer(
        f"💎 Тариф {tariff} — {info['name']}\n\n"
        f"Перейдіть за посиланням для оплати:\n"
        f"{link}"
    )
    await callback.answer()


# ================================
#    LiqPay CALLBACK handler
# ================================
async def liqpay_callback(request: web.Request):
    try:
        data = await request.post()
        print("🔥 CALLBACK RECEIVED:", data)

        lp_data = data.get("data")
        lp_sign = data.get("signature")

        if not lp_data:
            print("❌ CALLBACK ERROR: no data")
            return web.Response(text="no data")

        # Декодуємо JSON
        import base64, json
        decoded = json.loads(base64.b64decode(lp_data).decode())

        order_id = decoded.get("order_id")
        status = decoded.get("status")

        print("🔥 ORDER:", order_id, "| STATUS:", status)

    if status in ("success", "sandbox"):
    # expected format: userId_tariff_timestamp
            user_id, tariff, _ = order_id.split("_")

            set_tariff_for_user(int(user_id), tariff)
            print(f"✔ SUCCESS saved tariff {tariff} for user {user_id}")

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
