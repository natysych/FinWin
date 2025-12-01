from aiogram import Bot
from aiohttp import web
import base64
import json
from services.storage import get_tariff_for_user

async def liqpay_callback(request: web.Request):
    bot: Bot = request.app["bot"]

    data = await request.post()
    data_b64 = data.get("data")
    if not data_b64:
        return web.Response(text="NO DATA")

    decoded = json.loads(base64.b64decode(data_b64).decode())
    user_id = decoded.get("sender_phone")  # LiqPay НЕ передає user_id TG!

    # Ми НЕ можемо визначити Telegram ID через LiqPay!
    # Тому логіка проста: після оплати користувач сам вводить /survey

    return web.Response(text="OK")
