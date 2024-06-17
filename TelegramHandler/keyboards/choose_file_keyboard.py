from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
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

async def choose_file_kb_query(key_list: list, can_go_left: bool, can_go_right: bool) -> InlineKeyboardMarkup:
    nums_for_choose = [
        InlineKeyboardButton(
            text=str(x),
            callback_data=str(x)
        ) for x in range(1, key_list.__len__() + 1)
    ]
    rows = [
        nums_for_choose,
    ]
    if (can_go_left and can_go_right):
        rows.append([
            InlineKeyboardButton(
                text='⬅Назад',
                callback_data='prev'
            ),
            InlineKeyboardButton(
                text='Далее➡',
                callback_data='next'
            )
        ])

    elif (can_go_right):
        rows.append([
            InlineKeyboardButton(
                text='Далее➡',
                callback_data='next'
            )
        ])
    elif (can_go_left):
        rows.append([
            InlineKeyboardButton(
                text='⬅Назад',
                callback_data='prev'
            )
        ])
    rows.append([
        InlineKeyboardButton(
            text='Вернуться к выбору материалов',
            callback_data='menu_choose'
        )
    ])
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup

def download_file() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Получить шрифты")
    kb.button(text="В главное меню")
    return kb.as_markup(resize_keyboard=True)

def download_file_query() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text='Получить шрифты',
                callback_data='get_fonts'
            )
        ],
        [
            InlineKeyboardButton(
                text='В главное меню',
                callback_data='menu_choose'
            )
        ]

    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup

def back_in_last_state() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='back_in_state_last'
            )
        ],

    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


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

async def work_with_tags_query(key_list : list, can_go_left : bool,
                               can_go_right : bool, state : FSMContext) -> InlineKeyboardMarkup:
    user_info = await state.get_data()
    user_tags = user_info['user_tags']
    nums_for_choose = [
        InlineKeyboardButton(
            text=str(x),
            callback_data=str(x)
        ) for x in range(1, key_list.__len__() + 1)
    ]
    rows = [
        nums_for_choose,
    ]
    if (can_go_left and can_go_right):
        rows.append([
            InlineKeyboardButton(
                text='⬅Назад',
                callback_data='prev'
            ),
            InlineKeyboardButton(
                text='Далее➡',
                callback_data='next'
            )
        ])

    elif (can_go_right):
        rows.append([
            InlineKeyboardButton(
                text='Далее➡',
                callback_data='next'
            )
        ])
    elif (can_go_left):
        rows.append([
            InlineKeyboardButton(
                text='⬅Назад',
                callback_data='prev'
            )
        ])
    if (len(user_tags) > 0):
        rows.append([
            InlineKeyboardButton(
                text="Очистить теги",
                callback_data='clear_tags'
            )
        ])
    rows.append([
        InlineKeyboardButton(
            text="Найти слайды по введеным тегам",
            callback_data='find_with_tags'
        )
    ])
    rows.append([
        InlineKeyboardButton(
            text='Вернуться к выбору материалов',
            callback_data='menu_choose'
        )
    ])
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
