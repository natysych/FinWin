import os

TOKEN = os.getenv("BOT_TOKEN")

DOMAIN = os.getenv("DOMAIN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))
