from aiogram import Router, types
from services.storage import get_tariff_for_user

router = Router()

SURVEY_LINK = "https://forms.gle/yDwFQvB4CW5zPjNH6"


@router.message(commands=["survey"])
async def survey_start(message: types.Message):
    await message.answer(
        "📝 *Оплату отримано!*\n\n"
        "Заповніть, будь ласка, анкету, щоб ми могли зробити курс ще кориснішим 💛\n\n"
        f"👉 Анкета: {SURVEY_LINK}\n\n"
        "Коли закінчите — натисніть *Готово* 👇",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="✔️ Готово", callback_data="survey_done")]
            ]
        ),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data == "survey_done")
async def survey_done(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tariff = get_tariff_for_user(user_id)

    if not tariff:
        await callback.message.answer("Помилка: тариф не знайдено 😔")
        return

    from routers.payments import TARIFFS
    folder = TARIFFS[tariff]["folder"]

    await callback.message.answer(
        "🎉 Дякуємо за відповіді! ❤️\n\n"
        "Ось ваше посилання на курс:\n"
        f"👉 {folder}"
    )
    await callback.answer()
