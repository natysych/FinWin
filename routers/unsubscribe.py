# file: routers/unsubscribe.py
from aiogram import Router, types
from aiogram.filters import Command

from services.storage import set_unsubscribed

router = Router()


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: types.Message):
    user_id = message.from_user.id
    set_unsubscribed(user_id, True)
    await message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(lambda m: "unsubscribe" in m.text.lower())
async def text_unsubscribe(message: types.Message):
    user_id = message.from_user.id
    set_unsubscribed(user_id, True)
    await message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊",
        reply_markup=types.ReplyKeyboardRemove(),
    )
