import os

TOKEN = os.getenv("BOT_TOKEN")

DOMAIN = os.getenv("DOMAIN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

# --- LiqPay ---
LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")
LIQPAY_RESULT_URL = os.getenv("LIQPAY_RESULT_URL")  # повний URL до /payment/callback
