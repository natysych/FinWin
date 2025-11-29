from aiohttp import web
from aiogram import Bot
from config import TOKEN
from services.storage import set_tariff_for_user, set_unsubscribed

SURVEY_TEXT = (
    "🎉 Оплату отримано!\n"
    "Тепер заповніть анкету, щоб ми могли створити ще краще продукт для вас!\n\n"
    "📝 Заповнити анкету → /survey"
)


async def liqpay_callback(request: web.Request):
    data = await request.post()

    order_id = data.get("order_id")
    if not order_id:
        return web.Response(text="NO ORDER_ID")

    try:
        tariff, user_id_str = order_id.split("_")
        user_id = int(user_id_str)
    except Exception:
        return web.Response(text="BAD_ORDER_ID")

    # Статус — оплатив, тариф знаємо
    set_tariff_for_user(user_id, tariff)
    set_unsubscribed(user_id, False)

    bot = Bot(TOKEN)
    await bot.send_message(user_id, SURVEY_TEXT)

    return web.Response(text="OK")
