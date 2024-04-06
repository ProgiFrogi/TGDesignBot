from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

available_action = ["Удаление", "Добавление"]
available_category = ["Презентация", "Слайды", "Шрифты", "Структуры", "Изображения"]
available_walker = []

class Admin(StatesGroup):
    choosing_action = State()
    choosing_category = State()
    choosing_walker = State()
    choosing_download_before = State()
    choosing_download_after = State()
