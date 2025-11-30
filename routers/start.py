from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard
from services.storage import set_unsubscribed

router = Router()


# /start
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "🎉 *Вітаємо!*\n"
        "Ви підписалися на бот *FinanceForTeens*! 💛\n\n"
        "Це курс з фінансової грамотності для тих мрійників, "
        "які хочуть більше знань та системності на шляху до своїх ідей 🚀\n\n"
        "Ну як, цікаво? 😉"
    )

    await message.answer(text, reply_markup=start_keyboard(), parse_mode="Markdown")


# Натиснули «Так» після першого екрану
@router.callback_query(lambda c: c.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    text = (
        "📘 *Курс для підлітків 14–19 років!*\n\n"
        "У ньому поєднані:\n"
        "• 💰 фінансова грамотність\n"
        "• 💡 підприємництво\n"
        "• 🧠 логіка\n"
        "• ❤️ психологія\n\n"
        "Уроки подані у форматі *«від простого до складного»*, щоб допомогти:\n"
        "✨ зрозуміти свої цілі\n"
        "✨ побачити шлях до їх досягнення\n"
        "✨ надихнутися реальними історіями успіху\n\n"
        "Продовжимо? 👉"
    )

    await callback.message.answer(
        text, reply_markup=continue_keyboard(), parse_mode="Markdown"
    )


# Натиснули «Так, продовжимо» → показати тарифи
@router.callback_query(lambda c: c.data == "cont_yes")
async def continue_after_intro(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 *Оберіть формат участі:*",
        reply_markup=payment_type_keyboard(),
        parse_mode="Markdown",
    )


# Натиснули «Відписатись»
@router.callback_query(lambda c: c.data == "start_no")
async def unsubscribe(callback: types.CallbackQuery):
    set_unsubscribed(callback.from_user.id, True)

    await callback.message.answer(
        "Добре! Якщо передумаєте — просто напишіть */start* 😊",
        parse_mode="Markdown",
    )
