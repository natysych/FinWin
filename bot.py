import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Update

from config import TOKEN, WEBHOOK_URL

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router, liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

# Background reminders
from services.reminders import reminders_loop


async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інформація"),
        BotCommand(command="survey", description="Анкета"),
    ])

    print(f"🔗 Webhook successfully set: {WEBHOOK_URL}")


async def init_app():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)
    dp.include_router(unsubscribe_router)

    # aiohttp app
    app = web.Application()

    # Telegram webhook endpoint
    async def telegram_webhook(request: web.Request):
        print("=== WEBHOOK HIT ===")  # debug
        data = await request.json()
        print("RAW UPDATE:", data)
        update = Update.model_validate(data)

        await dp.feed_webhook_update(bot, update)
        return web.Response(text="OK")

    app.router.add_post("/webhook", telegram_webhook)

    # LiqPay callback
    app.router.add_post("/payment/callback", liqpay_callback)

    # Start background reminders
    asyncio.create_task(reminders_loop(bot))

    # Startup hook
    app.on_startup.append(lambda _: on_startup(bot))

    print("🚀 Application initialized. Awaiting Telegram updates...")
    return app


def main():
    app = asyncio.run(init_app())

    # Railway *must* use PORT env variable
    PORT = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting server on port {PORT}")

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
