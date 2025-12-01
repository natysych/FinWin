from aiogram import Router, types
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web
import time
import base64
import json

from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

# -----------------------------
#     ТАРИФИ
# -----------------------------
TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн"},
    "B": {"amount": 800,  "name": "Частинами — 800 грн (6 уроків)"},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн"},
    "D": {"amount": 3490, "name": "MAX — 3490 грн"},
}


# -----------------------------------------------------------
# 👉 ОБРОБКА ВИБОРУ ТАРИФУ → ГЕНЕРАЦІЯ LiqPay ПОСИЛАННЯ
# -----------------------------------------------------------
@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # Унікальний order_id
    order_id = f"{callback.from_user.id}_{int(time.time())}_{tariff}"

    # Зберегти тариф у локальній базі
    set_tariff_for_user(callback.from_user.id, tariff)

    # Створити зовнішній LiqPay-лінк
    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id
    )

    await callback.message.answer(
        f"💎 *Тариф {tariff} — {info['name']}*\n\n"
        f"🔗 Перейдіть за посиланням для оплати:\n{link}",
        parse_mode="Markdown"
    )

    await callback.answer()


# -----------------------------------------------------------
# 👉 CALLBACK LiqPay → після успішної оплати
# -----------------------------------------------------------
async def liqpay_callback(request: web.Request):
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

        # Якщо оплата успішна
        if status in ("success", "sandbox"):
            try:
                # Формат order_id: userID_timestamp_tariff
                parts = order_id.split("_")
                user_id = int(parts[0])
                tariff = parts[2]

                # Зберегти тариф
                set_tariff_for_user(user_id, tariff)
                print(f"✅ Tariff saved for user {user_id}: {tariff}")

                # Надсилаємо повідомлення
                from aiogram import Bot
                from config import TOKEN

                bot = Bot(token=TOKEN)

                await bot.send_message(
                    user_id,
                    "🎉 *Оплату отримано!*\n\n"
                    "Будь ласка, заповніть коротку анкету, щоб ми могли створити ще кращий продукт для вас 💛\n\n"
                    "📝 Анкета: https://forms.gle/yDwFQvB4CW5zPjNH6\n\n"
                    "Коли заповните — натисніть *Готово*.",
                    parse_mode="Markdown",
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="Готово")]],
                        resize_keyboard=True
                    )
                )

                await bot.session.close()

            except Exception as e:
                print("❌ Error during success-notification:", e)

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
