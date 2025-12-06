import time
import base64
import json

from aiohttp import web
from aiogram import Router, types, Bot
from aiogram.types import CallbackQuery

from config import TOKEN
from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()

TARIFFS = {
    "A": {"amount": 1500, "name": "Повна оплата — 1500 грн. Курс з 12 уроків, доступ назавжди."},
    "B": {"amount": 800, "name": "Оплата частинами — 800 грн, доступ до перших 6 уроків."},
    "C": {"amount": 2000, "name": "PRO доступ — 2000 грн. Весь курс + менторський супровід 1 місяць."},
    "D": {"amount": 3490, "name": "MAX-програма — 3490 грн. 6-місячна програма + додаткові модулі + спільнота + фідбек."},
}


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def pay_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    info = TARIFFS[tariff]

    # order_id: user_id_timestamp_tariff
    order_id = f"{callback.from_user.id}_{int(time.time())}_{tariff}"

    set_tariff_for_user(callback.from_user.id, tariff)

    link = create_payment_link(
        amount=info["amount"],
        description=f"Тариф {tariff}",
        order_id=order_id,
    )

    text = (
        f"💎 *Тариф {tariff}*\n"
        f"{info['name']}\n\n"
        f"🔗 Для оплати перейдіть за посиланням:\n{link}"
    )

    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()


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

        if status in ("success", "sandbox") and order_id:
            try:
                parts = order_id.split("_")
                user_id = int(parts[0])
                tariff = parts[2]

                set_tariff_for_user(user_id, tariff)
                print("✅ Tariff saved for user:", user_id, tariff)

                bot = Bot(token=TOKEN)

                await bot.send_message(
                    user_id,
                    "🎉 *Оплату отримано!*\n\n"
                    "Будь ласка, заповніть коротку анкету, щоб ми могли дати вам максимальну користь 💛\n\n"
                    "📝 Анкета: https://forms.gle/yDwFQvB4CW5zPjNH6\n\n"
                    "Коли заповните — натисніть кнопку *Готово* внизу.",
                    parse_mode="Markdown",
                )

                await bot.session.close()

            except Exception as e:
                print("❌ Failed to process successful payment:", e)

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
