import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

from routers.start import router as start_router
from routers.payments import router as payments_router
from routers.survey import router as survey_router
from routers.lessons import router as lessons_router


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Include routers
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(survey_router)
    dp.include_router(lessons_router)

    # aiohttp app
    app = web.Application()

    # Register webhook handler
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")

    # Setup application (shutdown, cleanup, polling off)
    setup_application(app, dp, bot=bot)

    # Set webhook
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook set:", WEBHOOK_URL)

    return app


if __name__ == "__main__":
    app = asyncio.run(main())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
