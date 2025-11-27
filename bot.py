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


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # --- Команди меню Telegram ---
    await bot.set_my_commands([
        BotCommand(command="start", description="
