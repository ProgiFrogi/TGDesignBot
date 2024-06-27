import json
import random

from TGDesignBot.utility.checkers import is_admin_with_json
from aiogram.fsm.context import FSMContext

from ...keyboards.start_and_simple_button import only_main_menu_button_kb, go_to_main_menu
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

router = Router()


class AdminState(StatesGroup):
    accept_add = State()
    input_id = State()


@router.callback_query(F.data == "new_admin_add",
                       lambda callback_query: is_admin_with_json(
                           callback_query.from_user.id))
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.input_id)
    text = "Введите id нового администратора"
    await callback_query.message.edit_text(
        text=text
    )


@router.message(AdminState.input_id)
async def first_depth_template_find(message: Message, state: FSMContext):
    await state.clear()
    with open("admins.json", "r") as file:
        config = json.load(file)
        if int(message.text) in config["admin_id"]:
            await message.answer(
                text='Данный пользователь уже является администратором!',
                reply_markup=only_main_menu_button_kb()
            )
            return
    await state.set_state(AdminState.accept_add)
    await state.update_data(new_admin_id=message.text)
    await message.delete()
    key = random.randint(100, 999)
    await state.update_data(key=str(key))
    text = f"Подтвердите добавление {message.text} отправив '{key}'"
    await message.answer(
        text=text,
        reply_markup=await go_to_main_menu()
    )


@router.message(AdminState.accept_add)
async def first_depth_template_find(message: Message, state: FSMContext):
    user_info = await state.get_data()
    key = user_info['key']
    new_admin_id = user_info['new_admin_id']

    if message.text != key:
        await message.answer(
            text='Введена неправильный код или команда',
            reply_markup=await go_to_main_menu()
        )
        return
    await state.clear()
    with open("admins.json", "r") as file:
        config = json.load(file)
        config["admin_id"].append(int(new_admin_id))
    with open("admins.json", "w") as file:
        json.dump(config, file)
    await message.answer(
        text=f'Пользователь {key} успешно добавлен!',
        reply_markup=only_main_menu_button_kb()
    )
