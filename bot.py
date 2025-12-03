import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router, liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

# Background tasks
from services.reminders import reminders_loop

# ──────────────────────────────────────────────
#  🔧 Monkey patch to suppress aiohttp timeout bug
# ──────────────────────────────────────────────
import aiohttp.client

_original_aenter = aiohttp.client._RequestContextManager.__aenter__

async def safe_aenter(self):
    """
    Fixes Railway webhook bug:
    "Timeout context manager should be used inside a task"
    """
    try:
        return await _original_aenter(self)
    except RuntimeError as e:
        if "Timeout context manager should be used inside a task" in str(e):
            print("⚠ Suppressed aiohttp timeout error")
            await asyncio.sleep(0)
            return await _original_aenter(self)
        raise e

aiohttp.client._RequestContextManager.__aenter__ = safe_aenter
# ──────────────────────────────────────────────


# ──────────────────────────────────────────────
#  BACKGROUND ANTI-SLEEP PING (Railway keep-alive)
# ──────────────────────────────────────────────
async def anti_sleep_ping(url: str):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.get(url)
                print("🌐 Ping → OK")
            except:
                print("⚠ Ping failed")
            await asyncio.sleep(60)   # пінгуємо кожну хвилину


# ──────────────────────────────────────────────
#  INITIALIZE APP
# ──────────────────────────────────────────────
async def init_app():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Bot commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інформація"),
        BotCommand(command="survey", description="Анкета"),
    ])

    # Routers
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)
    dp.include_router(unsubscribe_router)

    # Main web app
    app = web.Application()

    # LiqPay Callback
    app.router.add_post("/payment/callback", liqpay_callback)

    # Telegram Webhook
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    # Install webhook
    await bot.set_webhook(WEBHOOK_URL)
    print("🔗 Webhook installed:", WEBHOOK_URL)

    # Background jobs
    asyncio.create_task(reminders_loop(bot))
    print("⏰ Background workers started")

    # Anti-sleep ping for Railway
    asyncio.create_task(anti_sleep_ping(WEBHOOK_URL))

    return app


# ──────────────────────────────────────────────
#  ENTRYPOINT
# ──────────────────────────────────────────────
def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = loop.run_until_complete(init_app())

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
