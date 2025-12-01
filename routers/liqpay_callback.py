from aiohttp import web
import base64
import json
from services.storage import set_tariff_for_user


async def liqpay_callback(request: web.Request):
    data = await request.post()

    raw_data = data.get("data")
    signature = data.get("signature")

    if not raw_data:
        return web.Response(text="No data")

    # Декодуємо data
    decoded_json = base64.b64decode(raw_data).decode()
    payment_info = json.loads(decoded_json)

    print("📩 CALLBACK:", payment_info)  # 👉 тепер буде в логах

    order_id = payment_info.get("order_id")
    status = payment_info.get("status")

    # LiqPay статуси: success, failure, error, sandbox, wait_accept
    if status in ("success", "sandbox"):
        parts = order_id.split("_")
        user_id = parts[0]
        tariff = parts[1]

        set_tariff_for_user(user_id, tariff)

        return web.Response(text="OK")

    return web.Response(text="IGNORED")
