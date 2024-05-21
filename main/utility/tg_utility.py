from Repo.TGDesignBot.main.DBHandler import (get_templates_from_child_directories,
                                             get_fonts_from_child_directories,
                                             get_images_from_child_directories)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types
import io
import aiohttp
from aiogram.enums import ParseMode, ChatAction
from aiogram.utils.chat_action import ChatActionSender
import urllib.request
import os
import shutil
import zipfile

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
        list_of_files = await get_templates_from_child_directories(path)
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

async def send_zips(message : Message,  list_data):
    for_zip_path = f'Data/forZip'
    user_zip_path = for_zip_path + '/' + f'{message.from_user.id}'
    archive_name = f'{message.from_user.id}.zip'
    path_to_zip = for_zip_path + '/' + archive_name
    try:
        os.mkdir(user_zip_path)
        for file in list_data:
            urllib.request.urlretrieve(file[1], user_zip_path + f'/{file[3]}.zip')
        merge_fonts(user_zip_path, path_to_zip)
        await send_file_from_local(message, path_to_zip)
    except:
        message.answer(text='Извините, возникла техническая ошибка. Сообщите нам: example@mail.com и попробуйте позже')

    shutil.rmtree(user_zip_path)
    os.remove(path_to_zip)

# Enter the reply message, the path on Yadis, and the local path
# to download the files so that the bot sends the user the
# correct files
async def start_send_fonts(message : Message, YDpath):
    print(YDpath)
    list_fonts = get_fonts_from_child_directories(YDpath)
    if (len(list_fonts) == 0):
        await message.answer(
            text='По данному запросу не найдено ни одного шрифта!'
        )
    try:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )
    except:
        print('Error')
    try:
        async with ChatActionSender.upload_document(
            bot=message.bot,
            chat_id=message.chat.id,
        ):
            await send_zips(message, list_fonts)
    except:
        print('Error')

def merge_fonts(input_folder, output_zip):
    # Set for unique fonts
    unique_files = set()

    with zipfile.ZipFile(output_zip, 'w') as output_zip_file:
        dir_name = 'Fonts'
        output_zip_file.mkdir(dir_name)
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.zip'):
                    zip_file_path = os.path.join(root, file)
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        for font_file in zip_ref.namelist():
                            if font_file.endswith(('.otf', '.ttf')):
                                if font_file not in unique_files:
                                    unique_files.add(font_file)
                                    try:
                                        file_data = zip_ref.read(font_file)
                                        print(os.path.basename(font_file))
                                        output_zip_file.writestr(
                                            os.path.basename(font_file),
                                            file_data,
                                            compress_type=zipfile.ZIP_DEFLATED,
                                        )
                                    except:
                                        print('Cant add font to zip')


async def choose_message_from_type_file(message : Message, state : FSMContext, reply_markup):
    user_info = await state.get_data()
    type_file = user_info['type_file']

    if (type_file in ['template', 'slide']):
        await message.answer(
            text="Выберете один из файлов",
            reply_markup=reply_markup
        )
    elif(type_file == 'font'):
        await message.answer(
            text="Выберете презентацию из которой хотите получить ширфты",
            reply_markup=reply_markup
        )



if __name__ == '__main__':
    zip_f = '/home/proggifroggi/PycharmProjects/StudyProject/TGDesignBot/Repo/TGDesignBot/main/Data/forZip'
    folder = '/home/proggifroggi/PycharmProjects/StudyProject/TGDesignBot/Repo/TGDesignBot/main/Data/forZip/5592902615'
    zip_file = '/home/proggifroggi/PycharmProjects/StudyProject/TGDesignBot/Repo/TGDesignBot/main/Data/forZip/merged_fonts.zip'

    merge_fonts(folder, zip_file)


