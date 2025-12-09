import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router, liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

# Background reminders
from services.reminders import reminders_loop


# ------------------------------------------------------
# 🔧 Запуск при старті: встановлюємо webhook, команди
# ------------------------------------------------------
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інформація"),
        BotCommand(command="survey", description="Анкета"),
    ])

    print(f"🔗 Webhook successfully set: {WEBHOOK_URL}")


# ------------------------------------------------------
# 🌐 Ініціалізація AIOHTTP + Aiogram
# ------------------------------------------------------
async def init_app():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Підключаємо всі маршрути
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)
    dp.include_router(unsubscribe_router)

    # AIOHTTP app
    app = web.Application()

    # ---------------------------
    # Telegram Webhook endpoint
    # ---------------------------
    async def telegram_webhook(request: web.Request):
        data = await request.json()
        update = dp.update_handler.bot_update_class.model_validate(data)
        await dp.feed_update(bot, update)
        return web.Response()

    app.router.add_post("/webhook", telegram_webhook)

    # ---------------------------
    # LiqPay callback endpoint
    # ---------------------------
    app.router.add_post("/payment/callback", liqpay_callback)

    # ---------------------------
    # Background reminders
    # ---------------------------
    asyncio.create_task(reminders_loop(bot))

    # Startup hook — встановлюємо webhook
    app.on_startup.append(lambda _: on_startup(bot))

    print("🚀 Application initialized. Awaiting Telegram updates...")

    return app


# ------------------------------------------------------
# 🚀 Запуск сервера
# ------------------------------------------------------
def main():
    app = asyncio.run(init_app())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
