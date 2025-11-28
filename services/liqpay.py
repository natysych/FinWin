import base64
import hashlib
import json
import os

LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")
LIQPAY_RESULT_URL = os.getenv("LIQPAY_RESULT_URL")  # /payment/callback
LIQPAY_SERVER_URL = os.getenv("LIQPAY_SERVER_URL")  # цей можна не використовувати


def create_payment(amount, description, order_id):
    data = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "sandbox": 1,
        "result_url": LIQPAY_RESULT_URL,
        "server_url": LIQPAY_RESULT_URL,
    }

    data_json = json.dumps(data)
    data_b64 = base64.b64encode(data_json.encode()).decode()

    signature = hashlib.sha1(
        (LIQPAY_PRIVATE_KEY + data_b64 + LIQPAY_PRIVATE_KEY).encode()
    ).hexdigest()

    url = f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
    return url
