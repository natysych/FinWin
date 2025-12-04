from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from services.storage import set_user_state

router = Router()


# Кнопки Так / Ні
def yes_no_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Так")],
            [KeyboardButton(text="Ні")]
        ],
        resize_keyboard=True
    )


# ----------------------------------------
# /start
# ----------------------------------------
@router.message(Command("start"))
async def start_cmd(message: types.Message):

    text = (
        "👋 *Вітаємо!*\n"
        "Ви підписалися на бот *FinanceForTeens*!\n\n"
        "Це курс з фінансової грамотності, створений для мрійників, "
        "яким потрібна структура та знання, аби реалізувати свої ідеї.\n\n"
        "Ну як, цікаво?"
    )

    # Ставимо статус
    set_user_state(message.from_user.id, "welcome")

    await message.answer(
        text,
        reply_markup=yes_no_keyboard(),
        parse_mode="Markdown"
    )


# ----------------------------------------
# Якщо користувач натиснув «Так»
# ----------------------------------------
@router.message(lambda m: m.text == "Так")
async def user_yes(message: types.Message):

    set_user_state(message.from_user.id, "interested")

    text = (
        "Курс розрахований на підлітків 14–19 років.\n\n"
        "У ньому поєднані фінансова грамотність, підприємництво, логіка та психологія.\n"
        "Заняття побудовані від простого до складного.\n\n"
        "Готові продовжити?"
    )

    await message.answer(text, reply_markup=yes_no_keyboard())


# ----------------------------------------
# Якщо натиснули «Ні»
# ----------------------------------------
@router.message(lambda m: m.text == "Ні")
async def user_no(message: types.Message):

    set_user_state(message.from_user.id, "unsubscribed")

    await message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊",
        reply_markup=ReplyKeyboardRemove()
    )
