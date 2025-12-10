from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from services.storage import set_user_state

router = Router()


# ---------------------------
# INLINE КНОПКИ "Так / Ні"
# ---------------------------
def yes_no_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="Так", callback_data="yes"),
            InlineKeyboardButton(text="Ні", callback_data="no"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ---------------------------
# ХЕНДЛЕР /start
# ---------------------------
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
        reply_markup=yes_no_inline_keyboard(),
        parse_mode="Markdown",
    )


# ---------------------------
# КОРИСТУВАЧ НАТИСНУВ "ТАК"
# ---------------------------
@router.callback_query(F.data == "yes")
async def user_yes(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_user_state(user_id, "interested")

    text = (
        "Курс розрахований на підлітків 14–19 років.\n"
        "У ньому поєднані фінансова грамотність, основи підприємництва, логіка та психологія.\n\n"
        "Заняття побудовані у форматі «від простого до складного», щоб допомогти:\n"
        "• зрозуміти свої цілі\n"
        "• побачити шлях їх досягнення\n"
        "• надихнутися історіями успішних людей\n\n"
        "Продовжимо?"
    )

    await callback.answer()
    await callback.message.answer(
        text,
        reply_markup=yes_no_inline_keyboard(),
    )


# ---------------------------
# КОРИСТУВАЧ НАТИСНУВ "НІ"
# ---------------------------
@router.callback_query(F.data == "no")
async def user_no(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_user_state(user_id, "unsubscribed")

    await callback.answer()
    await callback.message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊"
    )
