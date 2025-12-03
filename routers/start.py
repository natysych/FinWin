from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard
import asyncio

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    # Важливо: виконувати відповідь через task, а не напряму
    asyncio.create_task(
        message.answer(
            "🎉 Вітаємо! Ви підписалися на FinanceForTeens!\n\n"
            "Хочете продовжити?",
            reply_markup=start_keyboard()
        )
    )


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


@router.callback_query(lambda c: c.data == "cont_yes")
async def show_tariffs(callback: types.CallbackQuery):
    from keyboards.pay_kb import payment_type_keyboard

    asyncio.create_task(
        callback.message.answer(
            "Оберіть тариф:",
            reply_markup=payment_type_keyboard()
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_no")
async def unsubscribe(callback: types.CallbackQuery):
    asyncio.create_task(
        callback.message.answer("😢 Ви відписалися.")
    )
    await callback.answer()
