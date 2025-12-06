from aiogram import Router, types
from aiogram.filters import Command

from services.storage import set_unsubscribed

router = Router()


@router.message(Command("unsubscribe"))
async def unsubscribe_cmd(message: types.Message):
    set_unsubscribed(message.from_user.id)

    await message.answer(
        "Ви відписалися від бота FinanceForTeens.\n"
        "Якщо захочете повернутися — просто напишіть /start 💛",
        reply_markup=types.ReplyKeyboardRemove(),
    )
