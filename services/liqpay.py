import base64
import hashlib
import json
from config import LIQPAY_PUBLIC, LIQPAY_PRIVATE

def create_payment(amount, description, order_id):
    data = {
        "public_key": LIQPAY_PUBLIC,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "sandbox": 1  # 0 → бойова версія
    }

    data_json = json.dumps(data)
    data_b64 = base64.b64encode(data_json.encode()).decode()

    signature = hashlib.sha1(
        (LIQPAY_PRIVATE + data_b64 + LIQPAY_PRIVATE).encode()
    ).hexdigest()

    url = f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
    return url
