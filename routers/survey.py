from aiogram import Router, types

router = Router()

@router.message(lambda m: m.text == "/survey")
async def survey_cmd(message: types.Message):
    await message.answer(
        "📝 Анкета перед стартом курсу:\n"
        "https://forms.gle/RexvvJbAQ2HP2YHr5"
    )
