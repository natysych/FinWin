from aiogram import Router, types
from services.storage import get_tariff_for_user

router = Router()

SURVEY_LINK = "https://forms.gle/yDwFQvB4CW5zPjNH6"

COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}


@router.message(commands=["survey"])
async def survey_start(message: types.Message):
    await message.answer(
        "🎉 Оплату отримано!\n"
        "Тепер заповніть анкету, щоб ми могли створити ще кращий продукт для вас!\n\n"
        f"📝 Анкета: {SURVEY_LINK}\n\n"
        "Коли заповните — натисніть *Готово*.",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Готово")]],
            resize_keyboard=True
        )
    )


@router.message(lambda m: m.text == "Готово")
async def send_course(message: types.Message):
    tariff = get_tariff_for_user(message.from_user.id)

    if not tariff:
        await message.answer("Помилка: не можу знайти ваш тариф 😢")
        return

    link = COURSE_LINKS.get(tariff)

    await message.answer(
        "Дякуємо за відповіді! ❤️\n\n"
        "Ось ваше посилання на курс:\n"
        f"👉 {link}",
        reply_markup=types.ReplyKeyboardRemove()
    )
