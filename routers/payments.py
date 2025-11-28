from aiogram import Router, types
from keyboards.pay_kb import payment_keyboard
from liqpay import create_payment

router = Router()

# --- Крок 1: користувач натиснув "Продовжити" ---
@router.callback_query(lambda c: c.data == "cont_yes")
async def choose_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "👇 Оберіть варіант оплати:",
        reply_markup=payment_keyboard()
    )


# --- Крок 2: Тарифи A/B/C/D ---
@router.callback_query(lambda c: c.data == "pay_A")
async def payment_A(callback: types.CallbackQuery):
    url = create_payment(
        amount=1500,
        description="Оплата тарифу A — FinanceForTeens",
        order_id="order_A"
    )
    await callback.message.answer(f"💳 Посилання на оплату:\n{url}")


@router.callback_query(lambda c: c.data == "pay_B")
async def payment_B(callback: types.CallbackQuery):
    url = create_payment(
        amount=800,
        description="Оплата тарифу B — FinanceForTeens",
        order_id="order_B"
    )
    await callback.message.answer(f"💳 Посилання на оплату:\n{url}")


@router.callback_query(lambda c: c.data == "pay_C")
async def payment_C(callback: types.CallbackQuery):
    url = create_payment(
        amount=2000,
        description="Оплата тарифу C — FinanceForTeens",
        order_id="order_C"
    )
    await callback.message.answer(f"💳 Посилання на оплату:\n{url}")


@router.callback_query(lambda c: c.data == "pay_D")
async def payment_D(callback: types.CallbackQuery):
    url = create_payment(
        amount=3490,
        description="Оплата тарифу D — FinanceForTeens",
        order_id="order_D"
    )
    await callback.message.answer(f"💳 Посилання на оплату:\n{url}")
