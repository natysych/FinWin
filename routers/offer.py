from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "offer")
async def send_offer(callback: types.CallbackQuery):
    with open("offer.pdf", "rb") as file:
        await callback.message.answer_document(
            document=file,
            caption="📄 Публічна оферта"
        )
