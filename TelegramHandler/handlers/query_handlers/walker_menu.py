import json
import pickle

from aiogram.filters import StateFilter

from TGDesignBot.utility.tg_utility import can_go_right as check_right, from_button_to_file, set_file_type, \
    choose_message_from_type_file, start_send_fonts, start_send_fonts_for_query, choose_message_from_type_file_query
from TGDesignBot.utility.tg_utility import can_go_left as check_left
from TGDesignBot.utility.tg_utility import can_go_back as check_back
from TGDesignBot.utility.tg_utility import update_data as update_user_info
from TGDesignBot.utility.tg_utility import update_indx as update_user_indx
from TGDesignBot.utility.tg_utility import get_list_of_files as get_list_of_files
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from ...keyboards.start_and_simple_button import choose_category_template, choose_catagory_text, \
    choose_catagory_callback, error_in_send_file
from ...keyboards.choose_file_keyboard import choose_file_kb, choose_file_kb_query
from ....Tree import ClassTree

router = Router()
users = [5592902615, 2114778573, 928962436, 986985057]

class WalkerState(StatesGroup):
    choose_button = State()
    choose_category = State()
    choose_file = State()

@router.callback_query(F.data == "pres_templates")
@router.callback_query(F.data == "slides")
@router.callback_query(F.data == "fonts")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        await state.clear()
        await state.set_state(WalkerState.choose_button)
        type_file = await set_file_type(callback_query.data, state)

        # take list of dirs
        child_list = tree.get_children(tree.root.name)

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)

        path = list()
        path.append(callback_query.data)
        await state.update_data(file_name_list=[])
        await update_user_info(state, path, 0, indx_list_end, False, child_list)
        print(indx_list_start, indx_list_end, child_list)
        reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, False, type_file)
        text = await choose_catagory_text(child_list[indx_list_start:indx_list_end])
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )


@router.callback_query(WalkerState.choose_button, F.data == "next")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']
        type_file = user_info['type_file']

        indx_list_start = indx_list_end
        indx_list_end = indx_list_end + dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, can_go_back, type_file)
        text = await choose_catagory_text(child_list[indx_list_start:indx_list_end])

        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)

@router.callback_query(WalkerState.choose_button, F.data == "prev")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        can_go_back = user_info['can_go_back']
        child_list = user_info['child_list']
        type_file = user_info['type_file']

        indx_list_start -= dist_indx
        indx_list_end -= dist_indx

        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)

        reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, can_go_back, type_file)
        text = await choose_catagory_text(child_list[indx_list_start:indx_list_end])

        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)

@router.callback_query(WalkerState.choose_button, F.data == "prev_dir")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        path = user_info['path']
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        child_list = user_info['child_list']
        type_file = user_info['type_file']

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx
        child_list = tree.get_children(tree.get_parent(path.pop(-1)))

        can_go_back = await check_back(path)
        can_go_right = await check_right(indx_list_end, len(child_list))
        can_go_left = await check_left(indx_list_start)
        reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, can_go_back, type_file)
        text = await choose_catagory_text(child_list[indx_list_start:indx_list_end])

        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )
        await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)

@router.callback_query(WalkerState.choose_button, F.data == "show_all_pres")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        path = user_info['path']
        child_list = user_info['child_list']

        indx_list_start = 0
        indx_list_end = indx_list_start + dist_indx

        files_list = await get_list_of_files(state)
        file_name_list = []

        for file in files_list:
            file_name_list.append(file[2])
        can_go_right = await check_right(indx_list_end, len(file_name_list))
        can_go_left = await check_left(indx_list_start)
        if len(file_name_list) != 0:
            reply_markup = await choose_file_kb_query(file_name_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right)
            text = await choose_catagory_text(file_name_list[indx_list_start:indx_list_end])
            await from_button_to_file(state, files_list, file_name_list, WalkerState.choose_file)
            await choose_message_from_type_file_query(callback_query, state, reply_markup, text)
        else:

            can_go_right = await check_right(indx_list_end, len(file_name_list))
            can_go_left = await check_left(indx_list_start)
            can_go_back = await check_back(path)
            type_file = user_info['type_file']

            reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, can_go_back, type_file)
            try:
                await callback_query.message.delete()
            except:
                pass
            await callback_query.bot.send_message(
                chat_id=callback_query.message.chat.id,
                text='В данной папке ничего нет!',
                reply_markup=reply_markup
            )


@router.callback_query(WalkerState.choose_button, F.data == "get_fonts_from_all_pres")
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    user_info = await state.get_data()
    path = '/'.join(user_info['path'][1:])
    try:
        await callback_query.message.edit_text(
            text="Дождитесь полной загрузки шрифтов..."
        )
    except:
        print('Proxy error')
    try:
        await start_send_fonts_for_query(callback_query, path)
    except:
        return
    try:
        reply_markup = await error_in_send_file()
        await callback_query.bot.send_message(
            chat_id=callback_query.message.chat.id,
            text='Все шрифты успешно отправлены!',
            reply_markup=reply_markup
        )
    except:
        print('Proxy error')

@router.callback_query(WalkerState.choose_button)
async def first_depth_template_find(callback_query : CallbackQuery, state: FSMContext):
    tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
    with open("config.json", "r") as file:
        user_info = await state.get_data()
        child_list = user_info['child_list']
        type_file = user_info['type_file']
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

        await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)

        reply_markup = await choose_catagory_callback(child_list[indx_list_start:indx_list_end], can_go_left,
                                                      can_go_right, can_go_back, type_file)
        text = await choose_catagory_text(child_list[indx_list_start:indx_list_end])

        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )