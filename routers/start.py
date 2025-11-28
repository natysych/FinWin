from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🎉 Вітаємо!\n\n"
        "Ви підписалися на FinanceForTeens — освітній бот із фінансової грамотності.\n\n"
        "Це курс для підлітків, які хочуть розуміти гроші, створювати власні ідеї та ставати самостійними.\n\n"
        "Ну що, цікаво?",
        reply_markup=start_keyboard()
    )


@router.callback_query(lambda c: c.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    await callback.message.answer(
        "📘 Інформація про курс\n\n"
        "Курс розрахований на підлітків 14–19 років. "
        "У ньому є фінансова грамотність, підприємництво, логіка, психологія.\n\n"
        "Готові продовжити?",
        reply_markup=continue_keyboard()
    )
