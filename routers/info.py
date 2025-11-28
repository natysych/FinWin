from aiogram import Router, types
from keyboards.info_kb import info_keyboard

router = Router()

@router.message(lambda m: m.text == "/info")
async def info_cmd(message: types.Message):
    await message.answer(
        "📍 *Контактна інформація:*\n\n"
        "👤 ФОП *Сич Наталія Вікторівна*\n"
        "📞 +380672899005\n"
        "🏠 м. Вишневе, вул. М. Примаченко, 25-б\n"
        "📧 finterra.com.ua@gmail.com\n\n"
        "📄 Публічна оферта: нижче кнопка",
        parse_mode="Markdown",
        reply_markup=info_keyboard()
    )
