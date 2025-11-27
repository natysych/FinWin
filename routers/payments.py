from aiogram import Router, types
from aiogram.filters import Text

from keyboards.pay_kb import payment_keyboard
from liqpay import create_payment

router = Router()

# --- Крок 1: користувач натиснув "Продовжити" ---
@router.callback_query(Text("cont_yes"))
async def choose_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 Оберіть варіант оплати:",
        reply_markup=payment_keyboard()
    )


# --- Крок 2: Тарифи A/B/C/D ---
@router.callback_query(Text("pay_A"))
async def pay_A(callback: types.CallbackQuery):
    url = create_payment(1500, "Оплата тарифу A", "order_A")
    await callback.message.answer(f"Посилання на оплату:\n{url}")

@router.callback_query(Text("pay_B"))
async def pay_B(callback: types.CallbackQuery):
    url = create_payment(800, "Оплата тарифу B", "order_B")
    await callback.message.answer(f"Посилання на оплату:\n{url}")

@router.callback_query(Text("pay_C"))
async def pay_C(callback: types.CallbackQuery):
    url = create_payment(2000, "Оплата тарифу C", "order_C")
    await callback.message.answer(f"Посилання на оплату:\n{url}")

@router.callback_query(Text("pay_D"))
async def pay_D(callback: types.CallbackQuery):
    url = create_payment(3490, "Оплата тарифу D", "order_D")
    await callback.message.answer(f"Посилання на оплату:\n{url}")
