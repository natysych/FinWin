from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("info"))
async def info_cmd(message: types.Message):
    await message.answer(
        "Це бот курсу FinanceForTeens. Інформаційний розділ буде доповнений пізніше."
    )
