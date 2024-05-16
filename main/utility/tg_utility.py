from Repo.TGDesignBot.main.DBHandler import (get_templates_from_child_directories,
                                             get_fonts_from_child_directories,
                                             get_images_from_child_directories)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types
import io
import aiohttp
from aiogram.enums import ChatAction
from aiogram.utils.chat_action import ChatActionSender

async def can_go_right(indx_list_end : int, len_child_list : int) -> bool:
    return indx_list_end < len_child_list


async def can_go_left(indx_list_start : int) -> bool:
    return indx_list_start != 0

async def can_go_back(user_data) -> bool:
    return not (len(user_data) == 0 or user_data[-1] == "Шаблон презентаций")

async def update_data(state : FSMContext, path, indx_list_start, indx_list_end, can_go_back, child_list) -> None:
    await state.update_data(path=path)
    await state.update_data(can_go_back=can_go_back)
    await state.update_data(child_list=child_list)
    await update_indx(state, indx_list_start, indx_list_end)

async def update_indx(state : FSMContext, indx_list_start, indx_list_end) -> None:
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

async def get_list_of_files(state : FSMContext) -> list:
    user_info = await state.get_data()
    list_of_path = user_info['path']

    # Check type of search
    if (list_of_path[0] == "Шаблон презентаций"):
        path = '/'.join(list_of_path[1:])
        list_of_files = await get_templates_from_child_directories(path)
    elif (list_of_path[0] == "Корпоративные шрифты"):
        path = '/'.join(list_of_path[1:])
        list_of_files = get_fonts_from_child_directories(path)
    elif (list_of_path[0] == "Изображения"):
        path = '/'.join(list_of_path[1:])
        list_of_files = get_images_from_child_directories(path)
    elif (list_of_path[0] == "Готовые слайды о компании"):
        path = '/'.join(list_of_path[1:])
        list_of_files = await get_templates_from_child_directories(path)
    return list_of_files

async def from_button_to_file(message : Message, state : FSMContext, files_list : list, file_name_list : list, to_state) -> None:
    global dist_indx
    user_info = await state.get_data()
    path = user_info['path']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']
    type_file = user_info['type_file']
    await state.set_state(to_state)
    await state.update_data(path=path)
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)
    await state.update_data(files_list=files_list)
    await state.update_data(file_name_list=file_name_list)
    await state.update_data(type_file=type_file)

async def admin_from_chose_dir_to_choose_file(message : Message, state : FSMContext, files_list : list, file_name_list : list, to_state) -> None:
    global dist_indx
    user_info = await state.get_data()
    path = user_info['path']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']
    await state.set_state(to_state)
    await state.update_data(path=path)
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)
    await state.update_data(files_list=files_list)
    await state.update_data(file_name_list=file_name_list)

async def set_file_type(message : Message, state : FSMContext) -> str:
    type_file = message.text

    if (type_file == "Шаблон презентаций"):
        await state.update_data(type_file='template')
        return 'template'
    elif (type_file == "Корпоративные шрифты"):
        await state.update_data(type_file='font')
        return 'font'
    elif (type_file == "Изображения"):
        await state.update_data(type_file='image')
        return 'image'
    elif (type_file == "Готовые слайды о компании"):
        await state.update_data(type_file='slide')
        return 'slide'
    return 'None'

async def send_big_file(message: types.Message, link, file_name):
    file = io.BytesIO()
    url = link
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename=f'{file_name}',
        ),
    )

async def download_with_link(message : Message, link, file_name):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await send_big_file(message, link, file_name)

async def send_file_from_local(message : Message, path):
    await message.reply_document(
        document=types.FSInputFile(
            path=path,
        )
    )
