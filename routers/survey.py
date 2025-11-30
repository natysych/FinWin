from aiogram import Router, types, F
from aiogram.filters import Command
from services.storage import get_tariff_for_user

router = Router()

SURVEY_URL = "https://forms.gle/yDwFQvB4CW5zPjNH6"

COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}


@router.message(Command("survey"))
async def survey_cmd(message: types.Message):
    await message.answer(
        f"📝 Анкета: {SURVEY_URL}\n\n"
        "Коли заповните анкету — натисніть кнопку «Готово» нижче.",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Готово ✔️", callback_data="survey_done")]
            ]
        ),
    )


@router.callback_query(F.data == "survey_done")
async def survey_done(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tariff = get_tariff_for_user(user_id)

    if not tariff or tariff not in COURSE_LINKS:
        await callback.message.answer(
            "Не вдалося визначити ваш тариф. Якщо помилка повторюється — напишіть, будь ласка, адміністратору."
        )
        return

    link = COURSE_LINKS[tariff]

    await callback.message.answer(
        "Дякуємо за відповіді! ❤️\n"
        "Ось ваше посилання на курс:\n"
        f"👉 {link}"
    )
