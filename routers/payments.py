# file: routers/payments.py
import time
import base64
import json

from aiohttp import web
from aiogram import Router, types
from aiogram.types import CallbackQuery

from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

# ---- ТАРИФИ ----
TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн"},
    "B": {"amount": 800, "name": "Оплата частинами — 800 грн"},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн"},
    "D": {"amount": 3490, "name": "MAX-програма — 3490 грн"},
}


# -----------------------------
# Вибір тарифу → створення лінку
# -----------------------------
@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # order_id включає user_id
    order_id = f"{callback.from_user.id}_{int(time.time())}_{tariff}"

    # Зберігаємо тариф
    set_tariff_for_user(callback.from_user.id, tariff)

    # Генеруємо LiqPay-лінк
    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id,
    )

    await callback.message.answer(
        f"💎 Тариф {tariff} — {info['name']}\n\n"
        f"Перейдіть за посиланням для оплати:\n{link}"
    )
    await callback.answer()


# -----------------------------
# LiqPay → callback /payment/callback
# -----------------------------
async def liqpay_callback(request: web.Request):
    """
    Обробляє POST-запит від LiqPay з полями {data, signature}.
    """
    try:
        payload = await request.post()
        print("🔥 CALLBACK RECEIVED:", payload)

        lp_data = payload.get("data")
        if not lp_data:
            return web.Response(text="no data")

        decoded = json.loads(base64.b64decode(lp_data).decode())
        order_id = decoded.get("order_id")
        status = decoded.get("status")

        print("🔥 ORDER:", order_id, "| STATUS:", status)

        if not order_id:
            return web.Response(text="no order_id")

        if status in ("success", "sandbox"):
            try:
                parts = order_id.split("_")
                user_id = int(parts[0])
                tariff = parts[-1]

                # ще раз зберігаємо тариф (на всяк випадок)
                set_tariff_for_user(user_id, tariff)
                print("✅ Tariff saved for user:", user_id, tariff)

                # надсилаємо користувачу повідомлення в Telegram
                from aiogram import Bot
                from config import TOKEN

                bot = Bot(token=TOKEN)
                await bot.send_message(
                    user_id,
                    "🎉 Оплату отримано!\n"
                    "Тепер заповніть анкету, щоб ми могли створити ще краще продукт для вас!\n\n"
                    "📝 Заповнити анкету → /survey"
                )
                await bot.session.close()

            except Exception as e:
                print("❌ Failed to notify user:", e)

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
