from aiogram import Router, types
from aiogram.filters import Command

from keyboards.start_kb import start_keyboard, continue_keyboard
from services.storage import set_unsubscribed

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "🎉 *Вітаємо!*\n"
        "Ви підписалися на бот *FinanceForTeens!* \n\n"
        "Це курс з фінансової грамотності. Він створений для тих мрійників, "
        "хто потребує додаткових знань та систематизації дій на шляху до реалізації своїх ідей!\n\n"
        "Ну як, цікаво? 😊"
    )

    await message.answer(
        text,
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data == "start_yes")
async def intro_part_two(callback: types.CallbackQuery):
    text = (
        "Курс розрахований на підлітків 14–19 років.\n"
        "У ньому поєднані фінансова грамотність, основи підприємництва, логіка та психологія.\n\n"
        "Заняття побудовані у форматі «від простого до складного», щоб допомогти:\n"
        "• зрозуміти свої цілі\n"
        "• побачити шлях їх досягнення\n"
        "• надихнутися історіями успішних людей\n\n"
        "Продовжимо?"
    )

    await callback.message.edit_text(
        text,
        reply_markup=continue_keyboard()
    )


@router.callback_query(lambda c: c.data == "start_no")
async def unsubscribe(callback: types.CallbackQuery):
    set_unsubscribed(callback.from_user.id, True)

    await callback.message.answer(
        "Добре! Якщо передумаєте — просто натисніть або напишіть /start 😊"
    )
