from aiogram import Router, types
from aiogram.filters import Text
from services.liqpay import create_payment

router = Router()

# --- ПОСИЛАННЯ НА КУРСИ ---
COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}

# --- АНКЕТА ---
SURVEY_URL = "https://forms.gle/yDwFQvB4CW5zPjNH6"


# --- Вибір тарифу ---
@router.callback_query(Text(startswith="pay_"))
async def process_payment(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]  # A / B / C / D

    pay_link = create_payment(
        amount=1500 if tariff == "A" else
                800 if tariff == "B" else
                2000 if tariff == "C" else
                3490,
        description=f"FinanceForTeens тариф {tariff}",
        order_id=f"{tariff}_{callback.from_user.id}"
    )

    await callback.message.answer(
        f"💳 Натисніть, щоб сплатити тариф {tariff}:\n{pay_link}"
    )


# --- LiqPay callback після оплати ---
@router.post("/payment/callback")
async def liqpay_callback(request):
    """
    LiqPay надсилає POST-запит після успішної оплати.
    """
    body = await request.post()

    # order_id у форматі "A_123456"
    order_id = body.get("order_id")
    if not order_id:
        return web.Response(text="No order_id")

    tariff = order_id.split("_")[0]  # A/B/C/D

    # --- Відповідь LiqPay має повертати 200 OK ---
    from aiogram import Bot
    from config import TOKEN

    bot = Bot(TOKEN)

    # ID юзера всередині order_id
    user_id = int(order_id.split("_")[1])

    await bot.send_message(
        user_id,
        "✅ Оплата отримана!\n"
        "Заповніть, будь ласка, анкету, щоб ми змогли дати вам більше користі 🙌\n\n"
        f"📝 Анкета: {SURVEY_URL}",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Готово ✔️", callback_data=f"done_{tariff}")]
        ])
    )

    return web.Response(text="OK")
