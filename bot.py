# file: bot.py
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

from routers.start import router as start_router
from routers.payments import router as payments_router, liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

from services.reminders import reminders_loop


async def init_app():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Команди бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інформація"),
        BotCommand(command="survey", description="Анкета"),
    ])

    # Підключаємо роутери
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)
    dp.include_router(unsubscribe_router)

    # Створюємо aiohttp-додаток
    app = web.Application()

    # LiqPay callback
    app.router.add_post("/payment/callback", liqpay_callback)

    # Telegram webhook
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    # Ставимо webhook
    await bot.set_webhook(WEBHOOK_URL)
    print("🔗 Webhook installed:", WEBHOOK_URL)

    # Фонові задачі
    asyncio.create_task(reminders_loop(bot))
    print("⏰ Background workers started")

    return app


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
