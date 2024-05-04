import pickle
from Repo.TGDesignBot.main.utility.tg_utility import can_go_right as check_right
from Repo.TGDesignBot.main.utility.tg_utility import can_go_left as check_left
from Repo.TGDesignBot.main.utility.tg_utility import can_go_back as check_back
from Repo.TGDesignBot.main.utility.tg_utility import update_data as update_user_info
from Repo.TGDesignBot.main.utility.tg_utility import update_indx as update_user_indx
from Repo.TGDesignBot.main.utility.tg_utility import get_list_of_files as get_list_of_files
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from ..keyboards.start_and_simple_button import choose_category_template
from ..keyboards.choose_file_keyboard import choose_file_kb
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
router = Router()

# try:
tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
# except:
#     # tree = ClassTree.Tree()
dist_indx = 1

class WalkerState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back
    choose_button = State()
    choose_category = State()
    choose_file = State()

# If user in root
@router.message(Command(commands=["depth_1_template"]))
@router.message(F.text.lower() == "шаблон презентаций")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx

    await state.clear()
    await state.set_state(WalkerState.choose_button)
    # take list of dirs
    child_list = tree.get_children(tree.root.name)

    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx

    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)

    path = list()
    path.append(message.text)
    await state.update_data(file_name_list=[])
    await update_user_info(state, path, 0, indx_list_end, False, child_list)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, False)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

@router.message(WalkerState.choose_button, F.text.lower() == "следующий блок")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx

    user_info = await state.get_data()
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    can_go_back = user_info['can_go_back']
    child_list = user_info['child_list']

    indx_list_start = indx_list_end
    indx_list_end = indx_list_end + dist_indx

    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await update_user_indx(state, indx_list_start, indx_list_end)

@router.message(WalkerState.choose_button, F.text.lower() == "преведущий блок")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    can_go_back = user_info['can_go_back']
    child_list = user_info['child_list']

    indx_list_start -= dist_indx
    indx_list_end -= dist_indx

    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)

    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await update_user_indx(state, indx_list_start, indx_list_end)

@router.message(WalkerState.choose_button, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    path = user_info['path']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']

    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx
    child_list = tree.get_children(tree.get_parent(path.pop(-1)))

    can_go_back = await check_back(path)
    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)

@router.message(WalkerState.choose_button, F.text.lower() == "вывести все")
async def output_files(message: Message, state: FSMContext):
    global dist_indx
    user_info = await state.get_data()
    path = user_info['path']

    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx

    files_list = await get_list_of_files(state)
    file_name_list = []

    for file in files_list:
        file_name_list.append(file[3])
    can_go_right = await check_right(indx_list_end, len(file_name_list))
    can_go_left = await check_left(indx_list_start)

    reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right)
    await from_button_to_file(message, state, files_list, file_name_list)
    await message.answer(
        text="Выберете один из файлов",
        reply_markup=reply_markup
    )

@router.message(WalkerState.choose_button)
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    child_list = user_info['child_list']

    if message.text not in child_list:
        return

    indx_list_start = 0
    indx_list_end = dist_indx + indx_list_start

    print(child_list)

    path = user_info['path']
    path.append(message.text)
    child_list = tree.get_children(message.text)
    can_go_back = await check_back(path)
    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)




@router.message(WalkerState.choose_button, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    path = user_info['path']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']

    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx
    child_list = tree.get_children(tree.get_parent(path.pop(-1)))

    can_go_back = await check_back(path)
    can_go_right = await check_right(indx_list_end, len(child_list))
    can_go_left = await check_left(indx_list_start)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await update_user_info(state, path, indx_list_start, indx_list_end, can_go_back, child_list)

async def from_button_to_file(message : Message, state : FSMContext, files_list : list, file_name_list : list) -> None:
    global dist_indx
    user_info = await state.get_data()
    path = user_info['path']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']
    await state.set_state(WalkerState.choose_file)
    await state.update_data(path=path)
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)
    await state.update_data(files_list=files_list)
    await state.update_data(file_name_list=file_name_list)