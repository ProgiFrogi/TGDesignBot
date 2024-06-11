from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def choose_file_kb(key_list: list, message: Message, can_go_left: bool,
                         can_go_right: bool) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=elem))
    kb.adjust(3)
    if (can_go_right):
        kb.button(text="Далее")
    if (can_go_left):
        kb.button(text="Назад")
    kb.adjust(2)
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def download_file(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Получить шрифты")
    kb.button(text="В главное меню")
    return kb.as_markup(resize_keyboard=True)


async def work_with_tags(key_list: list, can_go_left: bool,
                         can_go_right: bool, state: FSMContext) -> ReplyKeyboardMarkup:
    user_info = await state.get_data()
    user_tags = []
    user_tags = user_info['user_tags']
    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=elem))
    kb.adjust(3)
    if (can_go_right):
        kb.button(text="Далее")
    if (can_go_left):
        kb.button(text="Назад")
    kb.adjust(2)
    if (len(user_tags) > 0):
        kb.button(text="Очистить теги")
    kb.button(text="Найти слайды по введеным тегам")
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
