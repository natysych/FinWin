from aiogram import Router, types
from keyboards.pay_kb import payment_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "cont_yes")
async def choose_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 Оберіть варіант оплати:",
        reply_markup=payment_keyboard()
    )
