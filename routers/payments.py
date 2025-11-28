from aiogram import Router, types
from aiogram.filters import Text

router = Router()

@router.callback_query(Text("cont_yes"))
async def show_payments(callback: types.CallbackQuery):

    await callback.message.answer(
        "👇 Оберіть варіант оплати, щоб отримати доступ до курсу"
    )

    # --- ТАРИФ A ---
    await callback.message.answer(
        "💎 A) Повна оплата — 1500 грн\n"
        "12 уроків • доступ назавжди",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатити 1500 грн", url="https://www.liqpay.ua/?????")],
        ])
    )

    # --- ТАРИФ B ---
    await callback.message.answer(
        "💳 B) Оплата частинами — 800 грн\n"
        "Доступ до 6 уроків відразу після платежу.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатити 800 грн", url="https://www.liqpay.ua/?????")],
        ])
    )

    # --- ТАРИФ C ---
    await callback.message.answer(
        "🔥 C) PRO — 2000 грн\n"
        "Весь курс + менторський супровід 1 місяць.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатити 2000 грн", url="https://www.liqpay.ua/?????")],
        ])
    )

    # --- ТАРИФ D ---
    await callback.message.answer(
        "👑 D) MAX — 3490 грн\n"
        "6-місячна програма + додаткові модулі + спільнота + фідбек.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатити 3490 грн", url="https://www.liqpay.ua/?????")],
        ])
    )
