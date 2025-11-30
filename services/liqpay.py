import os
import json
import time
import base64
import hashlib


LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")
LIQPAY_RESULT_URL = os.getenv("LIQPAY_RESULT_URL")  # можна лишити як у тебе
# SERVER_URL зараз не використовуємо обов'язково


def _encode_data(data: dict) -> str:
    """Серіалізація даних LiqPay у base64."""
    data_json = json.dumps(data)
    return base64.b64encode(data_json.encode()).decode()


def _create_signature(data_b64: str) -> str:
    """Створення підпису LiqPay згідно їх документації."""
    sign_str = f"{LIQPAY_PRIVATE_KEY}{data_b64}{LIQPAY_PRIVATE_KEY}"
    sha1 = hashlib.sha1(sign_str.encode()).digest()
    return base64.b64encode(sha1).decode()


def create_payment_link(amount: int, description: str, order_id: str) -> str:
    """
    Створює посилання на сторінку оплати LiqPay.

    amount – сума в грн
    description – опис платежу
    order_id – унікальний ID замовлення
    """
    data = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "result_url": LIQPAY_RESULT_URL,
        "sandbox": 1,  # 1 = тестовий режим; 0 = бойовий
    }

    data_b64 = _encode_data(data)
    signature = _create_signature(data_b64)

    return f"https://www.liqpay.ua/api/3/checkout?data={data_b64}&signature={signature}"
