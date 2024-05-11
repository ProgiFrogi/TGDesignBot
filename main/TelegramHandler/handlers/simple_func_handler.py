from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.lower() == "стоп, а что ты умеешь?")
async def cmd_help(message: Message):
    await message.answer(
        "Я умею выводить нужные вам материалы, такие как шрифты, картинки или слайды, а также целые презентации!"
    )


@router.message(F.text.lower() == "хочу дать обратную связь")
async def cmd_feedback(message: Message):
    await message.reply(
        "Конечно, напишите нам: example@yandex.ru"
    )
