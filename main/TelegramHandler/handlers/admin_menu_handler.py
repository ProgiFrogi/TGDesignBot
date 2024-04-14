import pickle
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
from aiogram import F, Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..keyboards.start_and_simple_button import admin_panel
from aiogram.types import Message
from aiogram.fsm.state import default_state, StatesGroup, State
from ..keyboards.start_and_simple_button import start_menu_kb, choose_category_kb, admin_choose_category_template
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value, HashTag
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder
router = Router()

admins = [5592902615]

# try:
tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))
# except:
#     # tree = ClassTree.Tree()
dist_indx = 1
indx_list_start = 0
indx_list_end = indx_list_start + dist_indx
child_list = {"old"}

class AdminState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back, действие
    choose_button = State()

@router.message(F.text.lower() == "админ-панель", lambda message: message.from_user.id in admins)
async def admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AdminState.choose_button)
    await message.answer(
        text='Выберете действие',
        reply_markup=admin_panel(message)
    )

@router.message(F.text.lower() == "добавить материал", lambda message: message.from_user.id in admins)
async def admin_menu(message: Message, state: FSMContext):
    await state.update_data(state_action="add")
    await message.answer(
        text='Выберете папку',
        reply_markup=choose_category_kb(message)
    )
@router.message(F.text.lower() == "удалить материал", lambda message: message.from_user.id in admins)
async def admin_menu(message: Message, state: FSMContext):
    await state.update_data(state_action="delete")
    await message.answer(
        text='Выберете папку',
        reply_markup=choose_category_kb(message)
    )


async def set_default():
    global indx_list_start, indx_list_end, child_list, tree, dist_indx
    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx

# If user in root
@router.message(Command(commands=["depth_1_template"]))
@router.message(AdminState.choose_button, F.text.lower() == "шаблон презентаций")
async def first_depth_template_find(message: Message, state: FSMContext):
    global tree, dist_indx

    child_list = tree.get_children(tree.root.name)
    indx_list_start = 0
    indx_list_end = indx_list_start + dist_indx
    can_go_right, can_go_left = True, Tree
    if (indx_list_end >= len(child_list)):
        can_go_right = False
    if (indx_list_start == 0):
        can_go_left = False
    path = list()
    path.append(message.text)
    await state.update_data(user_node=path)
    await state.update_data(indx_list_start=0)
    print('Admin do smth')
    await state.update_data(can_go_back=False)
    await state.update_data(indx_list_end=indx_list_end)
    await state.update_data(child_list=child_list)
    user_info = await state.get_data()
    action = user_info['state_action']
    reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, False, action)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

# If user not in root
@router.message(Command(commands=["next_block"]))
@router.message(AdminState.choose_button, F.text.lower() == "следующий блок")
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
    user_info = await state.get_data()
    action = user_info['state_action']
    reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                  can_go_right, False, action)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

@router.message(Command(commands=["prev_block"]))
@router.message(AdminState.choose_button, F.text.lower() == "преведущий блок")
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
    user_info = await state.get_data()
    action = user_info['state_action']
    reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                        can_go_right, False, action)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )

    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

@router.message(AdminState.choose_button, F.text.lower() == "назад")
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
    user_info = await state.get_data()
    action = user_info['state_action']
    reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left,
                                                        can_go_right, False, action)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await state.update_data(can_go_back=can_go_back)

@router.message(F.document)
async def download_file(message : Message, bot : Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name.split('.')
    file = await bot.get_file(file_id)
    file_path = file.file_path
    # path = f"./Data/DataFromUser/"
    await bot.download_file(
        file_path,
        f"./Data/DataFromUser/{file_name[0]}.{file_name[-1]}"
    )

@router.message(F.text == '/r')
async def download_file(message : Message, bot : Bot):
    await bot.send_document(
        chat_id=message.chat.id,
        document=types.FSInputFile(
            path=f"./Data/Buffer/rofl.txt",
            filename='rofl'
        )
    )






@router.message(AdminState.choose_button)
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
    reply_markup = await admin_choose_category_template(child_list[indx_list_start:indx_list_end], message, can_go_left, can_go_right, can_go_back)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=reply_markup
    )
    await state.update_data(can_go_back=can_go_back)
    await state.update_data(child_list=child_list)

