from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.start_and_simple_button import start_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f'Приветствую, {message.from_user.first_name}. Я DesignBot. Чем я могу вам помочь?',
        reply_markup=start_menu(Message)
    )

@router.message(StateFilter(None), Command(commands=["menu"]))
@router.message(default_state, F.text.lower() == "главное меню")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Вы и так в главном меню...",
        reply_markup=start_menu(Message)
    )
@router.message(Command(commands=["menu"]))
@router.message(F.text.lower() == "главное меню")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Вы главном меню",
        reply_markup=start_menu(Message)
    )