from aiogram import Router, types
from aiogram.filters import Command
from keyboards.info_kb import info_keyboard

router = Router()

@router.message(Command("info"))
async def info_cmd(message: types.Message):
    await message.answer(
        "📍 *Контактна інформація:*\n\n"
        "👤 ФОП *Сич Наталія Вікторівна*\n"
        "📞 +380672899005\n"
        "🏠 м. Вишневе, вул. М. Примаченко, 25-б, кв.108\n"
        "✉ finterra.com.ua@gmail.com\n\n"
        "📚 *FinanceForTeens* — освітній проект компанії *Finterra*.\n"
        "ФОП 3-тя група (без ПДВ)\n\n"
        "📄 Публічна оферта доступна за посиланням нижче:",
        reply_markup=info_keyboard()
    )
