from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("survey"))
async def survey_cmd(message: types.Message):
    await message.answer(
        "📝 *Анкета перед стартом курсу*\n\n"
        "Будь ласка, заповніть коротку форму, щоб я могла краще адаптувати матеріал ❤️\n\n"
        "👉 Анкета: https://forms.gle/RexvvJbAQ2HP2YHr5",
        parse_mode="Markdown"
    )
