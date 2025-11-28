import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # --- Команди меню Telegram ---
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інфо/контакти"),
        BotCommand(command="survey", description="Анкета перед стартом"),
    ])

    # --- Підключення роутерів ---
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)

    # --- aiohttp app ---
    app = web.Application()

    # --- Register webhook handler ---
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")

    # --- Setup lifecycle ---
    setup_application(app, dp, bot=bot)

    # --- Set webhook ---
    await bot.set_webhook(WEBHOOK_URL)
    print("🔗 Webhook set:", WEBHOOK_URL)
    print("🤖 Bot is running...")

    return app


if __name__ == "__main__":
    web.run_app(main(), host=WEBAPP_HOST, port=WEBAPP_PORT)
