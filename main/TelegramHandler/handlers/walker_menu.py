import pickle

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from ..keyboards.start_and_simple_button import choose_category_template
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
router = Router()

# try:
tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
# except:
#     # tree = ClassTree.Tree()
dist_indx = 1
indx_list_start = 0
indx_list_end = indx_list_start + dist_indx
child_list = {"old"}


async def set_default():
    global indx_list_start, indx_list_end, child_list, tree, dist_indx
    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx

class WalkerState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back
    choose_button = State()

# If user in root
@router.message(Command(commands=["depth_1_template"]))
@router.message(F.text.lower() == "шаблон презентаций")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx, child_list
    await set_default()
    child_list = tree.get_children(tree.root.name)
    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx
    can_go_right, can_go_left = True, Tree
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    await state.clear()
    await state.set_state(WalkerState.choose_button)
    path = list()
    path.append(message.text)
    await state.update_data(user_node=path)
    await state.update_data(indx_list_start=0)
    print(indx_list_start)
    print(indx_list_end)
    await state.update_data(can_go_back=False)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, False)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

@router.message(Command(commands=["next_block"]))
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

    can_go_right, can_go_left = True, Tree
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

@router.message(Command(commands=["prev_block"]))
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

    can_go_right, can_go_left = True, Tree
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

@router.message(WalkerState.choose_button, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()
    user_data = user_info['user_node']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']

    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx
    child_list = tree.get_children(tree.get_parent(user_data.pop(-1)))
    await state.update_data(user_node=user_data)
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)

    can_go_right, can_go_left, can_go_back = True, True, True
    if (len(user_data) == 0 or user_data[-1] == "Шаблон презентаций"):
        can_go_back = False
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await state.update_data(can_go_back=can_go_back)


@router.message(WalkerState.choose_button)
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx
    user_info = await state.get_data()

    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    child_list = user_info['child_list']
    if message.text not in child_list:
        return
    user_data = user_info['user_node']
    user_data.append(message.text)
    await state.update_data(user_node=user_data)

    can_go_right, can_go_left, can_go_back = True, True, True
    child_list = tree.get_children(message.text)
    if (len(user_data) == 0 or user_data[-1] == "Шаблон презентаций"):
        can_go_back = False
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    reply_markup = await choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await state.update_data(can_go_back=can_go_back)
    await state.update_data(child_list=child_list)