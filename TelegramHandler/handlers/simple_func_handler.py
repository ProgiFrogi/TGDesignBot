import json

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(F.text.lower() == "стоп, а что ты умеешь?")
@router.message(Command("actions"))
async def cmd_help(message: Message):
    await message.answer(
        "Я умею выводить нужные вам материалы, такие как шрифты, слайды, а также целые презентации!"
    )


@router.message(Command("help"))
@router.message(F.text.lower() == "хочу дать обратную связь")
async def cmd_feedback(message: Message):
    await message.reply(
        f"Конечно, напишите нам: {json.load(open('./config.json'))['email']}"
    )
