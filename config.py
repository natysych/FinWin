import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

DOMAIN = os.getenv("DOMAIN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

LIQPAY_PUBLIC = os.getenv("LIQPAY_PUBLIC")
LIQPAY_PRIVATE = os.getenv("LIQPAY_PRIVATE")
