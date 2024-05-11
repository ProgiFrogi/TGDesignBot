from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

admins = [5592902615]

# Стартовое меню
def start_menu_kb(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Готовлю презентацию сам, нужны материалы")
    # kb.button(text="admin menu")
    kb.button(text="Стоп, а что ты умеешь?")
    kb.button(text="Хочу дать обратную связь")
    kb.adjust(1)
    if (message.from_user.id in admins):
        kb.button(text="Админ-панель")
    return kb.as_markup(resize_keyboard=True)
def only_main_menu_button_kb(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="В главное меню")
    return kb.as_markup(resize_keyboard=True)

def main_menu_kb(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Как установить шрифты?")
    kb.button(text="В главное меню")
    return kb.as_markup(resize_keyboard=True)
# Кнопки с выбором категорий
def choose_category_kb(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Шаблон презентаций")
    kb.button(text="Готовые слайды о компании")
    kb.button(text="Корпоративные шрифты")
    kb.button(text="Изображения")
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

async def choose_category_template(key_list : list, message : Message, can_go_left : bool, can_go_right : bool,
                                   can_go_back : bool, file_type : str) -> ReplyKeyboardMarkup:

    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=elem))
    kb.adjust(3)
    kb.button(text="Вывести все")
    if (file_type == 'font'):
        kb.button(text='Забрать все')
    kb.adjust(1)
    if (can_go_right):
        kb.button(text="Следующий блок")
    if (can_go_left):
        kb.button(text="Преведущий блок")
    kb.adjust(2)
    if (can_go_back):
        kb.button(text="Назад")
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

async def admin_choose_category_template(key_list : list, message : Message, can_go_left : bool, can_go_right : bool, can_go_back : bool, action : str) -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=elem))
    kb.adjust(3)
    print('admin_choose')
    if (action == 'delete'):
        kb.button(text="Вывести все")
        kb.adjust(1)
    if (action == 'add'):
        kb.button(text="Добавить сюда")
        kb.adjust(1)
    if (can_go_right):
        kb.button(text="Следующий блок")
    if (can_go_left):
        kb.button(text="Преведущий блок")
    kb.adjust(2)
    if (can_go_back):
        kb.button(text="Назад")
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_panel(message : Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить материал")
    kb.button(text="Удалить материал")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)