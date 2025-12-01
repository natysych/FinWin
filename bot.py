import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router
from routers.liqpay_callback import liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

# Background tasks
from services.reminders import reminders_loop


async def main():
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

    # WebApp
    app = web.Application()

    # LiqPay callback route
    app.router.add_post("/payment/callback", liqpay_callback)

    # Telegram webhook route
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    # Set webhook
    await bot.set_webhook(WEBHOOK_URL)
    print("🔗 Webhook set:", WEBHOOK_URL)

    # Background task
    asyncio.create_task(reminders_loop(bot))
    print("⏰ Reminders started")

    return app


if __name__ == "__main__":
    web.run_app(main(), host=WEBAPP_HOST, port=WEBAPP_PORT)
