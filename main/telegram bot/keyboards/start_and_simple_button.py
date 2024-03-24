from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message

# Стартовое меню
def start_menu(message: Message) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Готовлю презентацию сам, нужны материалы")
    kb.button(text="Редактировать материалы")
    # kb.button(text="admin menu")
    kb.button(text="Стоп, а что ты умеешь?")
    kb.button(text="Хочу дать обратную связь")
    print(Message.from_user.id)
    kb.button(text="Admin menu")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

# Кнопки с выбором категорий
def choose_category() ->ReplyKeyboardMarkup:
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