# file: routers/offer.py
from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.filters import Command

router = Router()


@router.callback_query(lambda c: c.data == "offer")
async def offer_callback(callback: types.CallbackQuery):
    # PDF оферти, наприклад: data/offer.pdf
    doc = FSInputFile("data/offer.pdf")
    await callback.message.answer_document(doc, caption="Публічна оферта")
    await callback.answer()


@router.message(Command("offer"))
async def offer_cmd(message: types.Message):
    doc = FSInputFile("data/offer.pdf")
    await message.answer_document(doc, caption="Публічна оферта")
