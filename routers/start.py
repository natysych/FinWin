from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard
from services.storage import set_unsubscribed

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🎉 Вітаємо! Ви підписалися на *FinanceForTeens*!",
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    await callback.message.answer(
        "📘 Курс 14–19 років\n\n✨ Фінанси\n✨ Підприємництво\n✨ Логіка\n✨ Психологія\n\nПродовжимо?",
        reply_markup=continue_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "cont_yes")
async def continue_after_intro(callback: types.CallbackQuery):
    from keyboards.pay_kb import payment_keyboard
    await callback.message.answer("Оберіть тариф:", reply_markup=payment_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_no")
async def unsubscribe(callback: types.CallbackQuery):
    set_unsubscribed(callback.from_user.id, True)
    await callback.message.answer("Добре! Якщо передумаєте — напишіть /start 😊")
    await callback.answer()
