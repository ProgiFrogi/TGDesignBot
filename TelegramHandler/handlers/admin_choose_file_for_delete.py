import json

from TGDesignBot.utility.tg_utility import can_go_right as check_right
from TGDesignBot.utility.tg_utility import can_go_left as check_left
from TGDesignBot.utility.tg_utility import update_indx as update_user_indx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from ..keyboards.choose_file_keyboard import choose_file_kb
from ...YandexDisk.YaDiskHandler import delete_from_disk

router = Router()


class AdminState(StatesGroup):
    # In the state we store child_list, indx_list_start\end, can_go_back
    choose_button = State()
    choose_category = State()
    choose_file = State()


@router.message(AdminState.choose_file, F.text.lower() == "далее")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        dist_indx = json.load(file)['dist']
        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        file_name_list = user_info['file_name_list']

        indx_list_start = indx_list_end
        indx_list_end = indx_list_end + dist_indx

        can_go_right = await check_right(indx_list_end, len(file_name_list))
        can_go_left = await check_left(indx_list_start)
        reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end],
                                            message,
                                            can_go_left,
                                            can_go_right)
        await message.answer(
            text="Выберите один из файлов",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(AdminState.choose_file, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        dist_indx = json.load(file)['dist']

        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        file_name_list = user_info['file_name_list']

        indx_list_start -= dist_indx
        indx_list_end -= dist_indx

        can_go_right = await check_right(indx_list_end, len(file_name_list))
        can_go_left = await check_left(indx_list_start)

        reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left,
                                            can_go_right)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(AdminState.choose_file)
async def choose_category(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        user_info = await state.get_data()
        file_name_list = user_info['file_name_list']
        if message.text not in file_name_list:
            await message.answer(
                text='Введена неправильная команда'
            )
            return
        await message.answer(
            text='Данный файл удаляется...'
        )
        link = None
        file_name = None
        file_path = None
        files_list = user_info['files_list']

        for file in files_list:
            if file[2] == message.text:
                file_id = file[0]
                file_path = file[1]
                file_name = file[2]
                await state.update_data(file_id=file_id)
                await state.update_data(link=link)
                await state.update_data(file_path=file_path)
                await state.update_data(file_name=file_name)
                break
        try:
            delete_from_disk(str(file_path) + '/' + str(file_name))
        except:
            pass
        await message.answer(
            text='Данный файл успешно удален!'
        )
