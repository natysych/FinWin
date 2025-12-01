from aiohttp import web
import json

from services.storage import set_tariff_for_user


async def liqpay_callback(request: web.Request):
    body = await request.post()
    data_b64 = body.get("data")
    if not data_b64:
        return web.Response(text="No data")

    try:
        data_json = json.loads(base64.b64decode(data_b64).decode("utf-8"))
    except Exception:
        return web.Response(text="Bad data")

    order_id = data_json.get("order_id")
    status = data_json.get("status")
    user_id = data_json.get("sender_phone") or None

    if status == "success" and order_id:
        # order_id format: USERID_TARIFF
        try:
            uid_str, tariff = order_id.split("_")
            uid = int(uid_str)

            set_tariff_for_user(uid, tariff)
        except:
            pass

    return web.Response(text="OK")
