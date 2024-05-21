from aiogram import Router, F
from aiogram.types import Message

router = Router()
users = [5592902615, 2114778573, 928962436]

@router.message(F.text.lower() == "стоп, а что ты умеешь?", lambda message: message.from_user.id in users)
async def cmd_help(message: Message):
    await message.answer(
        "Я умею выводить нужные вам материалы, такие как шрифты, картинки или слайды, а также целые презентации!"
    )
@router.message(F.text.lower() == "хочу дать обратную связь", lambda message: message.from_user.id in users)
async def cmd_feedback(message: Message):
    await message.reply(
        "Конечно, напишите нам: example@yandex.ru"
    )