import json
import os
import pickle

from TGDesignBot.utility.checkers import is_admin_with_json
from TGDesignBot.utility.tg_utility import can_go_right as check_right, get_list_of_files, \
    admin_from_chose_dir_to_choose_file
from TGDesignBot.utility.tg_utility import can_go_left as check_left
from TGDesignBot.utility.tg_utility import can_go_back as check_back
from TGDesignBot.utility.tg_utility import update_data as update_user_info
from TGDesignBot.utility.tg_utility import update_indx as update_user_indx
from TGDesignBot.YandexDisk.YaDiskHandler import upload_to_disk
from aiogram.fsm.context import FSMContext
import aiogram.exceptions as tg_exceptions

from ...keyboards import choose_file_kb_query
from ...keyboards.start_and_simple_button import admin_panel_query, admin_choose_category_template_query, \
    choose_tags_query, admin_add_here
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, F, Router
from aiogram.types import Message, CallbackQuery

router = Router()


class AdminState(StatesGroup):
    # In the state we store child_list, indx_list_start\end, can_go_back, and action.
    choose_button = State()
    choose_file = State()


@router.message(F.text.lower() == "админ-панель",
                lambda message: is_admin_with_json(message.from_user.id))
async def admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Выберите действие',
        reply_markup=admin_panel_query()
    )


# If user in root
@router.callback_query(F.data == "admin_add",
                       lambda callback_query: is_admin_with_json(callback_query.from_user.id))
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.choose_button)
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
        path.append(callback_query.data)
        await update_user_info(state, path, 0, indx_list_end, False, child_list)
        user_info = await state.get_data()
        action = user_info['state_action']
        await state.update_data()
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right,
                                                                  False,
                                                                  action)
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или скиньте ваш файл \n\n" + text,
            reply_markup=reply_markup
        )


@router.callback_query(F.data == "admin_delete",
                       lambda callback_query: is_admin_with_json(callback_query.from_user.id))
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.choose_button)
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
        path.append(callback_query.data)
        await update_user_info(state, path, 0, indx_list_end, False, child_list)
        user_info = await state.get_data()
        action = user_info['state_action']
        await state.update_data()
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right, False, action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )


@router.callback_query(AdminState.choose_button, F.data == "next")
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        user_info = await state.get_data()
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']

        indx_list_start = indx_list_end
        indx_list_end = indx_list_end + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        user_info = await state.get_data()
        action = user_info['state_action']
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right,
                                                                  can_go_back,
                                                                  action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )
        await update_user_indx(state, indx_list_start, indx_list_end)


@router.callback_query(AdminState.choose_button, F.data == "prev")
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
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
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right,
                                                                  can_go_back,
                                                                  action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.callback_query(AdminState.choose_button, F.data == "prev_dir")
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
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
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right, can_go_back, action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )
        await update_user_info(state, user_data, indx_list_start, indx_list_end, can_go_back, child_list)


@router.callback_query(AdminState.choose_button, F.data == "add_here")
async def first_depth_template_find(callback_query: CallbackQuery):
    reply_markup = admin_add_here()
    await callback_query.message.edit_text(
        text="Отправьте ваш файл в чат",
        reply_markup=reply_markup
    )


@router.callback_query(AdminState.choose_button, F.data == "step_back")
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        user_info = await state.get_data()
        action = user_info['state_action']
        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right,
                                                                  can_go_back,
                                                                  action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(F.document, AdminState.choose_button)
async def download_file(message: Message, bot: Bot, state: FSMContext):
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


@router.callback_query(AdminState.choose_button, F.data == "show_all_pres_for_delete")
async def output_files(callback_query: CallbackQuery, state: FSMContext):
    with open("./config.json", "r") as file:
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

        reply_markup = await choose_file_kb_query(file_name_list[indx_list_start:indx_list_end], can_go_left,
                                                  can_go_right)
        text = await choose_tags_query(file_name_list[indx_list_start:indx_list_end])
        await admin_from_chose_dir_to_choose_file(state, files_list, file_name_list, AdminState.choose_file)
        await callback_query.message.edit_text(
            text="Выберите один из файлов для удаления \n\n" + text,
            reply_markup=reply_markup
        )


@router.callback_query(AdminState.choose_button)
async def first_depth_template_find(callback_query: CallbackQuery, state: FSMContext):
    tree = pickle.load(open("./Tree/ObjectTree.pkl", "rb"))
    with open("./config.json", "r") as file:
        user_info = await state.get_data()
        child_list = user_info['child_list']
        indx_list_start = user_info['indx_list_start']

        path = user_info['path']

        indx_child = indx_list_start + int(callback_query.data) - 1

        path.append(child_list[indx_child])
        child_list = tree.get_children(child_list[indx_child])

        indx_list_start = 0
        config = json.load(file)
        dist_indx = config['dist']
        indx_list_end = dist_indx + indx_list_start

        can_go_back = await check_back(path)
        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        action = user_info['state_action']

        await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)

        reply_markup = await admin_choose_category_template_query(child_list[indx_list_start:indx_list_end],
                                                                  can_go_left,
                                                                  can_go_right, can_go_back, action)
        text = await choose_tags_query(child_list[indx_list_start:indx_list_end])

        await callback_query.message.edit_text(
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы \n\n" + text,
            reply_markup=reply_markup
        )
