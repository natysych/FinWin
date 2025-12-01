from aiogram import Router, types
from aiogram.filters import Command
from services.storage import get_tariff_for_user
from config import SURVEY_LINK, FULL_COURSE, HALF_COURSE

router = Router()


@router.message(Command("survey"))
async def survey_start(message: types.Message):
    await message.answer(
        "📝 Дякуємо за оплату!\n"
        "Будь ласка, заповніть невелику анкету — це допоможе нам краще зрозуміти ваші цілі ❤️\n\n"
        f"👉 Анкета: {SURVEY_LINK}\n\n"
        "Коли будете готові — натисніть кнопку нижче 👇",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="Готово ✅",
                    callback_data="survey_done"
                )
            ]]
        )
    )


@router.callback_query(lambda c: c.data == "survey_done")
async def survey_done(call: types.CallbackQuery):
    user_id = call.from_user.id
    tariff = get_tariff_for_user(user_id)

    if tariff == "A":
        link = FULL_COURSE
    elif tariff == "B":
        link = HALF_COURSE
    elif tariff == "C":
        link = FULL_COURSE
    elif tariff == "D":
        link = FULL_COURSE
    else:
        await call.message.edit_text("❗ Виникла помилка. Тариф не знайдено.")
        return

    await call.message.edit_text(
        "🎉 Дякуємо! Анкету отримано ❤️\n\n"
        "Ось ваше посилання на курс:\n"
        f"👉 {link}\n\n"
        "Успіхів у навчанні! 🚀"
    )
