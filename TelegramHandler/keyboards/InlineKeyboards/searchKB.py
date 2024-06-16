from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def build_choose_kb() -> InlineKeyboardMarkup:
    templates = InlineKeyboardButton(
        text='Шаблон презентаций',
        callback_data='pres_templates'
    )
    slides = InlineKeyboardButton(
        text='Готовые слайды о компании',
        callback_data='slides'
    )
    fonts = InlineKeyboardButton(
        text='Корпоративные шрифты',
        callback_data='fonts'
    )
    rows = [
        [templates],
        [slides],
        [fonts],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup