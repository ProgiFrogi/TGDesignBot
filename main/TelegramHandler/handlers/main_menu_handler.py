from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from ..keyboards.start_and_simple_button import start_menu_kb, choose_category_kb

router = Router()



class UserStates(StatesGroup):
    in_main_menu = State()
    in_choose_category = State()
    find_images = State()
    find_templates = State()
    find_slides_about_company = State()
    find_fonts = State()
    find_ready_structs = State()


@router.message(Command("start"))
async def cmd_start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f'Приветствую, {message.from_user.first_name}. Я DesignBot. Чем я могу вам помочь?',
        reply_markup=start_menu_kb(message)
    )

@router.message(StateFilter(default_state), Command(commands=["menu"]))
@router.message(default_state, F.text.lower() == "в главное меню")
async def cmd_cancel_handler(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Вы и так в главном меню...",
        reply_markup=start_menu_kb(message)
    )
@router.message(Command(commands=["menu"]))
@router.message(F.text.lower() == "в главное меню")
async def cmd_cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Вы в главном меню",
        reply_markup=start_menu_kb(message)
    )

@router.message(StateFilter(None), Command(commands=["choose_category"]))
@router.message(F.text.lower() == "готовлю презентацию сам, нужны материалы")
async def choose_category_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Что вас интересует?",
        reply_markup=choose_category_kb(message)
    )
    await state.set_state(UserStates.in_choose_category)


