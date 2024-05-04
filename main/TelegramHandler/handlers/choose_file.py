import pickle
from Repo.TGDesignBot.main.utility.tg_utility import can_go_right as check_right
from Repo.TGDesignBot.main.utility.tg_utility import can_go_left as check_left
from Repo.TGDesignBot.main.utility.tg_utility import update_indx as update_user_indx
from aiogram.utils.chat_action import ChatActionSender
from aiogram import types
import io
import aiohttp
from aiogram.enums import ParseMode, ChatAction
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from ..keyboards.choose_file_keyboard import choose_file_kb

router = Router()

dist_indx = 1
class WalkerState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back
    choose_button = State()
    choose_category = State()
    choose_file = State()

@router.message(WalkerState.choose_file, F.text.lower() == "следующий блок")
async def first_depth_template_find(message: Message, state: FSMContext):
    global dist_indx

    user_info = await state.get_data()
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    file_name_list = user_info['file_name_list']

    indx_list_start = indx_list_end
    indx_list_end = indx_list_end + dist_indx

    can_go_right = await check_right(indx_list_end, len(file_name_list))
    can_go_left = await check_left(indx_list_start)
    reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await update_user_indx(state, indx_list_start, indx_list_end)

@router.message(WalkerState.choose_file, F.text.lower() == "преведущий блок")
async def first_depth_template_find(message: Message, state: FSMContext):
    global dist_indx

    user_info = await state.get_data()
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    file_name_list = user_info['file_name_list']

    indx_list_start -= dist_indx
    indx_list_end -= dist_indx

    can_go_right = await check_right(indx_list_end, len(file_name_list))
    can_go_left = await check_left(indx_list_start)

    reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await update_user_indx(state, indx_list_start, indx_list_end)

@router.message(WalkerState.choose_file)
async def choose_category(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    file_name_list = user_info['file_name_list']
    if message.text not in file_name_list:
        return

    files_list = user_info['files_list']
    for file in files_list:
        if file[3] == message.text:
            link = file[1]
            break
    await message.answer(
        text="Ваш файл загружается..."
    )
    await download_with_link(message, link)

async def send_big_file(message: types.Message, link):
    file = io.BytesIO()
    url = link
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename="file.pptx",
        ),
    )

async def download_with_link(message : Message, link):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await send_big_file(message, link)
