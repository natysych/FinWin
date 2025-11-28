import base64
import hashlib
import json
from config import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY

def create_payment(amount, description, order_id):
    data = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "sandbox": 1
    }

    data_json = json.dumps(data)
    data_b64 = base64.b64encode(data_json.encode()).decode()

    signature = hashlib.sha1(
        (LIQPAY_PRIVATE_KEY + data_b64 + LIQPAY_PRIVATE_KEY).encode()
    ).hexdigest()

    return f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
