from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from services.storage import set_user_state

router = Router()


def yes_no_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Так")],
            [KeyboardButton(text="Ні")],
        ],
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "👋 *Вітаємо!*\n"
        "Ви підписалися на бот *FinanceForTeens*! \n"
        "Це курс з фінансової грамотності. Він створений для тих мрійників, "
        "хто потребує додаткових знань та систематизації дій на шляху до реалізації своїх ідей!\n\n"
        "Ну як, цікаво?"
    )

    set_user_state(message.from_user.id, "welcome")

    await message.answer(
        text,
        reply_markup=yes_no_keyboard(),
        parse_mode="Markdown",
    )


@router.message(lambda m: m.text == "Так")
async def user_yes(message: types.Message):
    set_user_state(message.from_user.id, "interested")

    text = (
        "Курс розрахований на підлітків 14–19 років.\n"
        "У ньому поєднані фінансова грамотність, основи підприємництва, логіка та психологія.\n\n"
        "Заняття побудовані у форматі «від простого до складного», щоб допомогти:\n"
        "• зрозуміти свої цілі\n"
        "• побачити шлях їх досягнення\n"
        "• надихнутися історіями успішних людей\n\n"
        "Продовжимо?"
    )

    await message.answer(
        text,
        reply_markup=yes_no_keyboard(),
    )


@router.message(lambda m: m.text == "Ні")
async def user_no(message: types.Message):
    set_user_state(message.from_user.id, "unsubscribed")

    await message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊",
        reply_markup=types.ReplyKeyboardRemove(),
    )
