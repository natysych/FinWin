import base64
import hashlib
import json
import os


LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")


def create_payment(amount, description, order_id):
    data = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "result_url": os.getenv("LIQPAY_RESULT_URL"),
        "server_url": os.getenv("LIQPAY_SERVER_URL"),
        "sandbox": 1
    }

    data_json = json.dumps(data)
    data_b64 = base64.b64encode(data_json.encode()).decode()

    to_sign = LIQPAY_PRIVATE_KEY + data_b64 + LIQPAY_PRIVATE_KEY
    signature = base64.b64encode(hashlib.sha1(to_sign.encode()).digest()).decode()

    return f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
