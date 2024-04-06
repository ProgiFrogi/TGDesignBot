
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message

# Стартовое меню
def start_menu_kb(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Готовлю презентацию сам, нужны материалы")
    # kb.button(text="admin menu")
    kb.button(text="Стоп, а что ты умеешь?")
    kb.button(text="Хочу дать обратную связь")
    kb.button(text="Admin menu")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)



# Кнопки с выбором категорий
def choose_category_kb(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Шаблон презентаций")
    kb.button(text="Готовые слайды о компании")
    kb.button(text="Корпоративные шрифты")
    kb.button(text="Готовые структуры")
    kb.button(text="Изображения")
    kb.button(text="В главное меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)




# Если получилось
def admin_menu_step_1() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Шаблон презентаций")
    kb.button(text="Готовые слайды о компании")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

async def choose_category_template(key_list : list, message : Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for elem in key_list:
        kb.add(types.KeyboardButton(text=str(elem)))
    kb.adjust(3)
    kb.button(text="Вывести все")
    kb.button(text="Следующий блок")
    kb.button(text="Назад")
    kb.button(text="Главное меню")
    kb.adjust(1)
    await message.answer(
        "Выберите папку:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )