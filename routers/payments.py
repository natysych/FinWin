from aiogram import Router, types

router = Router()

# --- ТВОЇ ГОТОВІ ЗОВНІШНІ LiqPay ПОСИЛАННЯ ---
PAY_LINK_A = "ТУТ ЛІНК A"
PAY_LINK_B = "ТУТ ЛІНК B"
PAY_LINK_C = "ТУТ ЛІНК C"
PAY_LINK_D = "ТУТ ЛІНК D"


@router.callback_query(lambda c: c.data == "pay_A")
async def pay_A(callback: types.CallbackQuery):
    await callback.message.answer(
        "💎 Тариф A — Повна оплата 1500 грн\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{PAY_LINK_A}"
    )


@router.callback_query(lambda c: c.data == "pay_B")
async def pay_B(callback: types.CallbackQuery):
    await callback.message.answer(
        "💳 Тариф B — Частинами 800 грн\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{PAY_LINK_B}"
    )


@router.callback_query(lambda c: c.data == "pay_C")
async def pay_C(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔥 Тариф C — PRO доступ 2000 грн\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{PAY_LINK_C}"
    )


@router.callback_query(lambda c: c.data == "pay_D")
async def pay_D(callback: types.CallbackQuery):
    await callback.message.answer(
        "👑 Тариф D — MAX програма 3490 грн\n"
        "Перейдіть за посиланням для оплати:\n"
        f"{PAY_LINK_D}"
    )
