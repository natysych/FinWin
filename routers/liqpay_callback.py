from aiohttp import web
from aiogram import Bot, types
from config import TOKEN
import json

SURVEY_URL = "https://forms.gle/yDwFQvB4CW5zPjNH6"

COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}

async def liqpay_callback(request: web.Request):
    data = await request.post()

    order_id = data.get("order_id")
    if not order_id:
        return web.Response(text="NO ORDER_ID")

    tariff, user_id = order_id.split("_")
    user_id = int(user_id)

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
        ),
    )

    return web.Response(text="OK")
