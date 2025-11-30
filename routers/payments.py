@router.post("/payment/callback")
async def liqpay_callback(request: web.Request):
    try:
        form = await request.post()
        data_b64 = form.get("data")
        signature = form.get("signature")

        if not data_b64 or not signature:
            return web.Response(text="no data")

        # Validate signature
        check = hashlib.sha1(f"{LIQPAY_PRIVATE_KEY}{data_b64}{LIQPAY_PRIVATE_KEY}".encode()).digest()
        check_b64 = base64.b64encode(check).decode()

        if check_b64 != signature:
            return web.Response(text="invalid signature")

        # Decode data
        data_json = base64.b64decode(data_b64).decode()
        data = json.loads(data_json)

        status = data.get("status")
        user_id = int(data.get("order_id").split("_")[0])
        tariff = data.get("order_id").split("_")[1]

        if status == "success":
            set_tariff_for_user(user_id, tariff)

            await bot.send_message(
                user_id,
                "🎉 *Оплату отримано!*\n\n"
                "Тепер заповніть анкету, щоб ми могли створити ще кращий продукт для вас!",
                parse_mode="Markdown"
            )

            await bot.send_message(
                user_id,
                "📝 *Анкета:* https://forms.gle/yDwFQvB4CW5zPjNH6",
                parse_mode="Markdown"
            )

        return web.Response(text="ok")

    except Exception as e:
        return web.Response(text=f"error: {e}")
