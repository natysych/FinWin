from aiogram import Router, types

from keyboards.pay_kb import payment_keyboard
from services.liqpay import create_payment_link
from services.storage import set_tariff_for_user

router = Router()


# /pay – показуємо вибір тарифів (якщо тобі треба окрема команда)
@router.message(lambda m: m.text == "/pay")
async def show_tariffs(message: types.Message):
    await message.answer(
        "👇 У нас є декілька форматів, оберіть той, що підходить вам найбільше. "
        "Після оплати ми попросимо заповнити анкету та надішлемо доступ до курсу.",
        reply_markup=payment_keyboard()
    )


# --- Тариф A -------------------------------------------------
@router.callback_query(lambda c: c.data == "pay_A")
async def pay_a(callback: types.CallbackQuery):
    # запам’ятовуємо тариф користувача
    set_tariff_for_user(callback.from_user.id, "A")

    pay_url = create_payment_link(
        amount=1500,
        description="Тариф A: Повна оплата — 1500 грн",
        order_id=f"{callback.from_user.id}_A",
    )

    await callback.message.answer(
        "💎 A) Повна оплата — 1500 грн.\n"
        "Курс з 12 уроків, доступ назавжди.\n\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{pay_url}"
    )


# --- Тариф B -------------------------------------------------
@router.callback_query(lambda c: c.data == "pay_B")
async def pay_b(callback: types.CallbackQuery):
    set_tariff_for_user(callback.from_user.id, "B")

    pay_url = create_payment_link(
        amount=800,
        description="Тариф B: Оплата частинами — 800 грн",
        order_id=f"{callback.from_user.id}_B",
    )

    await callback.message.answer(
        "💳 B) Оплата частинами — 800 грн.\n"
        "Доступ до перших 6 уроків відкриється одразу після платежу.\n\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{pay_url}"
    )


# --- Тариф C -------------------------------------------------
@router.callback_query(lambda c: c.data == "pay_C")
async def pay_c(callback: types.CallbackQuery):
    set_tariff_for_user(callback.from_user.id, "C")

    pay_url = create_payment_link(
        amount=2000,
        description="Тариф C: PRO доступ — 2000 грн",
        order_id=f"{callback.from_user.id}_C",
    )

    await callback.message.answer(
        "🔥 C) PRO доступ — 2000 грн.\n"
        "Доступ до всього курсу + менторський супровід 1 місяць.\n\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{pay_url}"
    )


# --- Тариф D -------------------------------------------------
@router.callback_query(lambda c: c.data == "pay_D")
async def pay_d(callback: types.CallbackQuery):
    set_tariff_for_user(callback.from_user.id, "D")

    pay_url = create_payment_link(
        amount=3490,
        description="Тариф D: MAX програма — 3490 грн",
        order_id=f"{callback.from_user.id}_D",
    )

    await callback.message.answer(
        "👑 D) MAX-програма — 3490 грн.\n"
        "6-місячна програма + додаткові модулі + спільнота + фідбек.\n\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{pay_url}"
    )
