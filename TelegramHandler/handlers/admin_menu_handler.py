import json
import os
import pickle
from TGDesignBot.utility.tg_utility import can_go_right as check_right, get_list_of_files, \
    from_button_to_file, admin_from_chose_dir_to_choose_file
from TGDesignBot.utility.tg_utility import can_go_left as check_left
from TGDesignBot.utility.tg_utility import can_go_back as check_back
from TGDesignBot.utility.tg_utility import update_data as update_user_info
from TGDesignBot.utility.tg_utility import update_indx as update_user_indx
from TGDesignBot.DBHandler import is_user_admin
from TGDesignBot.YandexDisk.YaDiskHandler import upload_to_disk
from aiogram.fsm.context import FSMContext
import aiogram.exceptions as tg_exceptions

from ..keyboards import choose_file_kb
from ..keyboards.start_and_simple_button import admin_panel
from aiogram.fsm.state import StatesGroup, State
from ..keyboards.start_and_simple_button import choose_category_kb, admin_choose_category_template
from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# Listing all admins
admins = [5592902615, 2114778573]
# try:

# YaDiskHandler.update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
# except:
#     tree = Tree()
#     YaDiskHandler.update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))

class AdminState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back, действие
    choose_button = State()
    choose_file = State()


@router.message(F.text.lower() == "админ-панель",
                lambda message: is_user_admin(message.from_user.id) or message.from_user.id in admins)
async def admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Выберите действие',
        reply_markup=admin_panel(message)
    )


# If user in root
@router.message(F.text.lower() == "добавить материал",
                lambda message: is_user_admin(message.from_user.id) or message.from_user.id in admins)
async def first_depth_template_find(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.choose_button)
    await message.answer(
        text='Выберите действие',
        reply_markup=admin_panel(message)
    )
    with open("config.json", "r") as file:
        dist_indx = json.load(file)['dist']
        await state.update_data(state_action="add")
        tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))

        child_list = tree.get_children(tree.root.name)

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)

        path = list()
        path.append(message.text)
        await update_user_info(state, path, 0, indx_list_end, False, child_list)
        user_info = await state.get_data()
        action = user_info['state_action']
        await state.update_data()
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                      can_go_right, False, action)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )


@router.message(F.text.lower() == "удалить материал",
                lambda message: is_user_admin(message.from_user.id) or message.from_user.id in admins)
async def admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.choose_button)
    await message.answer(
        text='Выберите действие',
        reply_markup=admin_panel(message)
    )
    await state.update_data(state_action="delete")
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        dist_indx = json.load(file)['dist']

        child_list = tree.get_children(tree.root.name)

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)

        path = list()
        path.append(message.text)
        await update_user_info(state, path, 0, indx_list_end, False, child_list)
        user_info = await state.get_data()
        action = user_info['state_action']
        await state.update_data()
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                      can_go_right, False, action)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )


@router.message(AdminState.choose_button, F.text.lower() == "далее")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']

        indx_list_start = indx_list_end
        indx_list_end = indx_list_end + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        user_info = await state.get_data()
        action = user_info['state_action']
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                      can_go_right, can_go_back, action)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )
        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(AdminState.choose_button, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']

        indx_list_start -= dist_indx
        indx_list_end -= dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        user_info = await state.get_data()
        action = user_info['state_action']
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                            can_go_right, False, action)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(AdminState.choose_button, F.text.lower() == "в предыдущую директорию")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
        user_info = await state.get_data()
        user_data = user_info['path']
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        child_list = user_info['child_list']

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx
        child_list = tree.get_children(tree.get_parent(user_data.pop(-1)))
        can_go_back = await check_back(user_data)
        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        user_info = await state.get_data()
        action = user_info['state_action']
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                            can_go_right, False, action)
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )
        await update_user_info(state, user_data, indx_list_start, indx_list_end, can_go_back, child_list)

@router.message(F.text.lower() == "добавить сюда", AdminState.choose_button)
async def download(message: Message, state: FSMContext):
    await message.answer(
        text="Скиньте ваш файл в чат",
    )

@router.message(F.text.lower() == "добавить сюда")
async def download(message: Message, state: FSMContext):
    await message.answer(
        text="Скиньте ваш файл в чат",
    )


@router.message(F.document, AdminState.choose_button)
async def download_file(message : Message, bot : Bot, state: FSMContext):
    user_info = await state.get_data()
    ydisk_path = user_info['path'][1:]
    file_id = message.document.file_id
    file_name = message.document.file_name.split('.')
    local_path = None
    try:
        file = await bot.get_file(file_id)
    except tg_exceptions.TelegramBadRequest:
        await message.answer(
            text='Ваш файл слишком большой: Telegram server says - Bad Request: file is' +
                 ' too big \n Вы можете попробовать загрузить другой файл'
        )
        return
    try:
        file_path = file.file_path
        local_path = f"./Data/DataFromUser/{file_name[0]}.{file_name[-1]}"
        await bot.download_file(
            file_path,
            local_path
        )
        upload_to_disk(ydisk_path, local_path)
    except:
        os.remove(local_path)
        await message.answer(
            text='Данный файл нельзя добавить здесь! Измените место добавления или название файла'
        )
    os.remove(local_path)
    await message.answer(
        text='Ваш файл успешно загружен!'
    )


@router.message(AdminState.choose_button, F.text.lower() == "показать все презентации")
async def output_files(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        path = user_info['path']

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx

        files_list = await get_list_of_files(state)
        file_name_list = []

        for file in files_list:
            file_name_list.append(file[2])
        can_go_right = await check_right(indx_list_end, len(file_name_list))
        can_go_left = await check_left(indx_list_start)

        reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left,
                                            can_go_right)
        await admin_from_chose_dir_to_choose_file(message, state, files_list, file_name_list, AdminState.choose_file)
        await message.answer(
            text="Выберите один из файлов",
            reply_markup=reply_markup
        )

@router.message(AdminState.choose_button)
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        child_list = user_info['child_list']

        if message.text not in child_list:
            await message.answer(
                text="Простите, я не понимаю =("
            )
            return

        indx_list_start = 0
        indx_list_end = dist_indx + indx_list_start

        user_data = user_info['path']
        user_data.append(message.text)
        child_list = tree.get_children(message.text)
        can_go_back = await check_back(user_data)
        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                            can_go_right, can_go_back, user_info['state_action'])
        await message.answer(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )
        await update_user_info(state, user_data, indx_list_start, indx_list_end, can_go_back, child_list)
