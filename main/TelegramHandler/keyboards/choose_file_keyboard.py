from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message

async def choose_file_kb(key_list : list, message : Message, can_go_left : bool,
                         can_go_right : bool) -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=elem))
    kb.adjust(3)
    kb.adjust(1)
    if (can_go_right):
        kb.button(text="Следующий блок")
    if (can_go_left):
        kb.button(text="Преведущий блок")
    kb.adjust(2)
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)