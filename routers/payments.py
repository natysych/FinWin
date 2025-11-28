from aiogram import Router, types, F
from services.liqpay import create_payment
from aiohttp import web

router = Router()

# --- ПОСИЛАННЯ НА КУРСИ ---
COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}

SURVEY_URL = "https://forms.gle/yDwFQvB4CW5zPjNH6"


# --- Обробка кнопок тарифів ---
@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]

    amount = {
        "A": 1500,
        "B": 800,
        "C": 2000,
        "D": 3490
    }[tariff]

    pay_link = create_payment(
        amount=amount,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=f"{tariff}_{callback.from_user.id}"
    )

    await callback.message.answer(
        f"💳 Натисніть, щоб сплатити тариф {tariff}:\n{pay_link}"
    )


# --- LiqPay callback ---
@router.post("/payment/callback")
async def liqpay_callback(request):
    body = await request.post()
    order_id = body.get("order_id")

    if not order_id:
        return web.Response(text="NO ORDER_ID")

    tariff, user_id = order_id.split("_")
    user_id = int(user_id)

    from aiogram import Bot
    from config import TOKEN
    bot = Bot(TOKEN)

    await bot.send_message(
        user_id,
        "✅ Оплата отримана!\n"
        "Заповніть, будь ласка, анкету, щоб ми могли дати вам більше користі 🙌\n\n"
        f"📝 Анкета: {SURVEY_URL}",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Готово ✔️", callback_data=f"done_{tariff}")]
            ]
        )
    )

    return web.Response(text="OK")
