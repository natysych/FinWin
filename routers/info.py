from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("info"))
async def info_cmd(message: types.Message):
    text = (
        "💼 *FinanceForTeens* — освітній проєкт компанії *Finterra*.\n\n"
        "👤 ФОП *Сич Наталія Вікторівна*\n"
        "📌 ФОП 3-тя група (без ПДВ)\n\n"
        "📞 +380672899005\n"
        "📧 finterra.com.ua@gmail.com\n\n"
        "📄 Публічна оферта доступна в меню «Оплата»"
    )

    await message.answer(text, parse_mode="Markdown")
