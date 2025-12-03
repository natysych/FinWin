from aiogram import Router, types
from aiogram.filters import Command
import asyncio

from keyboards.start_kb import start_keyboard, continue_keyboard
from keyboards.pay_kb import payment_type_keyboard

router = Router()


# -------------------------------
# /start
# -------------------------------
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    asyncio.create_task(
        message.answer(
            "🎉 Вітаємо! Ви підписалися на FinanceForTeens!\n\n"
            "Хочете продовжити?",
            reply_markup=start_keyboard()
        )
    )


# -------------------------------
# Натиснув «Так»
# -------------------------------
@router.callback_query(lambda c: c.data == "start_yes")
async def continue_after_intro(callback: types.CallbackQuery):
    asyncio.create_task(
        callback.message.answer(
            "Курс розрахований на підлітків 14–19 років.\n"
            "У ньому поєднані фінансова грамотність, основи підприємництва, логіка та психологія.\n\n"
            "Продовжимо?",
            reply_markup=continue_keyboard()
        )
    )
    await callback.answer()


# -------------------------------
# Натиснув «Так, продовжимо»
# -------------------------------
@router.callback_query(lambda c: c.data == "cont_yes")
async def show_tariffs(callback: types.CallbackQuery):
    asyncio.create_task(
        callback.message.answer(
            "Оберіть тариф 👇",
            reply_markup=payment_type_keyboard()
        )
    )
    await callback.answer()


# -------------------------------
# Натиснув «Ні»
# -------------------------------
@router.callback_query(lambda c: c.data == "start_no")
async def unsub(callback: types.CallbackQuery):
    asyncio.create_task(
        callback.message.answer("😢 Ви відписалися.")
    )
    await callback.answer()
