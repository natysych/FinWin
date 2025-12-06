import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import TOKEN, WEBAPP_HOST, WEBAPP_PORT

# Routers
from routers.start import router as start_router
from routers.payments import router as payments_router, liqpay_callback
from routers.info import router as info_router
from routers.survey import router as survey_router
from routers.offer import router as offer_router
from routers.unsubscribe import router as unsubscribe_router

# Background tasks
from services.reminders import reminders_loop


async def init_app():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Команди
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати"),
        BotCommand(command="info", description="Інформація"),
        BotCommand(command="survey", description="Анкета"),
    ])

    # Роутери
    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(info_router)
    dp.include_router(survey_router)
    dp.include_router(offer_router)
    dp.include_router(unsubscribe_router)

    # Aiohttp-сервер тільки для LiqPay callback
    app = web.Application()
    app.router.add_post("/payment/callback", liqpay_callback)

    # Фонова задача з нагадуваннями
    asyncio.create_task(reminders_loop(bot))

    # Запускаємо long polling у фоні
    asyncio.create_task(dp.start_polling(bot))

    print("🤖 BOT STARTED IN LONG POLLING MODE")
    print("🌐 LiqPay callback enabled at /payment/callback")

    return app


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
