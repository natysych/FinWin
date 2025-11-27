from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🎉 Вітаємо! Ви підписалися на бот FinanceForTeens!\n\n"
        "Це курс з фінансової грамотності...",
        reply_markup=start_keyboard()
    )

@router.callback_query(lambda c: c.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Інформація на курс розрахована на 14–19 років 📚\n..."
    )
    await callback.message.answer(
        "Продовжимо навчання?",
        reply_markup=continue_keyboard()
    )
