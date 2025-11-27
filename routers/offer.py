from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "offer")
async def send_offer(callback: types.CallbackQuery):
    await callback.message.answer_document(
        document=open("offer.pdf", "rb"),
        caption="📄 Публічна оферта"
    )
