from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("offer"))
async def offer_cmd(message: types.Message):
    await message.answer(
        "📄 Публічний договір-оферта доступний на сайті *Finterra*.\n"
        "Якщо посилання ще не підключене — напишіть Наталії, і вона все надішле 😊",
        parse_mode="Markdown",
    )
