from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_kb import start_keyboard, continue_keyboard
from services.storage import set_unsubscribed

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🎉 Вітаємо!\n"
        "Ви підписалися на бот *FinanceForTeens*!\n\n"
        "Це курс з фінансової грамотності — для мрійників, які хочуть системи дій та нових знань 😊\n"
        "Ну як, цікаво?",
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data == "start_yes")
async def start_yes(callback: types.CallbackQuery):
    await callback.message.answer(
        "📘 *Курс розрахований на підлітків 14–19 років.*\n\n"
        "У ньому поєднані:\n"
        "• фінансова грамотність\n"
        "• основи підприємництва\n"
        "• логіка\n"
        "• психологія\n\n"
        "Уроки допоможуть:\n"
        "✨ зрозуміти свої цілі\n"
        "✨ побачити шлях до них\n"
        "✨ надихнутися історіями успішних людей\n\n"
        "Продовжимо? 👉",
        reply_markup=continue_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_no")
async def unsubscribe(callback: types.CallbackQuery):
    set_unsubscribed(callback.from_user.id, True)

    await callback.message.answer(
        "Добре! Якщо передумаєте — просто напишіть /start 😊"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "cont_yes")
async def continue_after_intro(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 У нас є декілька форматів, оберіть той, що підходить вам найбільше.\n"
        "Після оплати ми попросимо заповнити анкету та надішлемо доступ до курсу."
    )

    # ВАЖЛИВО: тут немає payment_type_keyboard
    from keyboards.pay_kb import payment_keyboard
    await callback.message.answer(
        "Оберіть тариф:",
        reply_markup=payment_keyboard()
    )

    await callback.answer()
