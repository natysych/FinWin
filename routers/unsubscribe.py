from aiogram import Router, types, F
from services.storage import set_unsubscribed

router = Router()


@router.callback_query(F.data == "unsubscribe")
async def handle_unsubscribe(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    set_unsubscribed(user_id, True)

    await callback.message.answer(
        "Добре! Якщо передумаєте — просто натисніть або напишіть /start 😊"
    )
