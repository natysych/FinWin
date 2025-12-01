async def liqpay_callback(request: web.Request):
    """
    LiqPay надсилає POST { data, signature } після оплати.
    """
    try:
        payload = await request.post()

        lp_data = payload.get("data")
        lp_sign = payload.get("signature")

        print("🔥 CALLBACK RECEIVED:", payload)

        if not lp_data:
            return web.Response(text="no data")

        # Декодуємо JSON з LiqPay
        decoded = json.loads(base64.b64decode(lp_data).decode())

        order_id = decoded.get("order_id")
        status = decoded.get("status")

        print("🔥 ORDER:", order_id, "| STATUS:", status)

        # Якщо оплата успішна
        if status in ("success", "sandbox"):
            try:
                # Формат: userID_timestamp_tariff
                parts = order_id.split("_")
                user_id = int(parts[0])
                tariff = parts[2]

                # Зберігаємо тариф
                set_tariff_for_user(user_id, tariff)
                print("✅ Tariff saved for user:", user_id, tariff)

                # ---- НАДСИЛАЄМО ПОВІДОМЛЕННЯ З КНОПКОЮ "Готово" ----
                from aiogram import Bot
                from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
                from config import TOKEN

                bot = Bot(token=TOKEN)

                await bot.send_message(
                    user_id,
                    "🎉 *Оплату отримано!*\n\n"
                    "Будь ласка, заповніть коротку анкету, щоб ми могли створити ще кращий продукт для вас 💛\n\n"
                    "📝 Анкета: https://forms.gle/yDwFQvB4CW5zPjNH6\n\n"
                    "Коли заповните — натисніть *Готово*.",
                    parse_mode="Markdown",
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="Готово")]],
                        resize_keyboard=True
                    )
                )

                await bot.session.close()

            except Exception as e:
                print("❌ Failed to notify user:", e)

        return web.Response(text="ok")

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)
        return web.Response(text="error", status=500)
