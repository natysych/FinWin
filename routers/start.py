from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.start_kb import start_keyboard, continue_keyboard

router = Router()

# --- Хендлер команди /start ---
@router.message(CommandStart())
async def start_cmd(message: types.Message):
    text = (
        "🎉 <b>Вітаємо!</b>\n"
        "<b>Ви підписалися на бот FinanceForTeens!</b>\n\n"
        "Це курс з фінансової грамотності..."
    )

    await message.answer(
        text,
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )


# --- Обробка кнопки “Так, хочу почати” ---
@router.callback_query(F.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    text = (
        "Інформація на курс розрахована на <b>14–19 років</b> 📚\n"
        "..."
    )

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer(
        "Продовжимо навчання?",
        reply_markup=continue_keyboard()
    )
