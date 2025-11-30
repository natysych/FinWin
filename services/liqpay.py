import base64
import hashlib
import json

from config import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY, LIQPAY_RESULT_URL


def create_payment(amount, description, order_id):
    data = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "sandbox": 1,  # тестовий режим
        "result_url": LIQPAY_RESULT_URL,  # куди повертаємо юзера після оплати
        "server_url": LIQPAY_RESULT_URL,  # куди LiqPay шле callback
    }

    json_data = json.dumps(data)
    data_b64 = base64.b64encode(json_data.encode()).decode()

    # Правильний підпис для LiqPay: base64( sha1( private + data + private ) )
    to_sign = LIQPAY_PRIVATE_KEY + data_b64 + LIQPAY_PRIVATE_KEY
    sha1_hash = hashlib.sha1(to_sign.encode()).digest()
    signature = base64.b64encode(sha1_hash).decode()

    # URL на оплату
    return f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
