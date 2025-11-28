from aiogram import Router, types, F

router = Router()

COURSE_LINKS = {
    "A": "https://drive.google.com/drive/folders/17kRu8_6PUcvBqn8wu_VOfPF1yIX2MnjV",
    "B": "https://drive.google.com/drive/folders/1NOTy5kUv7A-t4733L-pTPFxNTZH3_GqJ",
    "C": "https://drive.google.com/drive/folders/12qIxBwxPzb8exbdONy6UX55mu-LP4P-6",
    "D": "https://drive.google.com/drive/folders/1pWH01RL1A7L9XK_Te1lwTLlIbVOx_BWQ",
}


@router.callback_query(F.data.startswith("done_"))
async def send_course(callback: types.CallbackQuery):
    tariff = callback.data.split("_")[1]
    link = COURSE_LINKS[tariff]

    await callback.message.answer(
        "🎉 Дякуємо!\nОсь ваш доступ до курсу: 👇\n" + link
    )
