from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def no_handled(message: Message):
    await message.answer(
        text="Простите, я не понимаю =("
    )
