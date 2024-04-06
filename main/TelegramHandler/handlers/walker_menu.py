import pickle

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import sys
sys.path.append(r"../../Tree/ClassTree.py")
from ..keyboards.start_and_simple_button import start_menu_kb, choose_category_kb, choose_category_template

router = Router()
tree = pickle.load(open("../../Tree/ObjectTree.pkl", "rb"))
dist_indx = 9
indx_list_start = 0
indx_list_end = indx_list_start + dist_indx

class WalkerState(StatesGroup):
    first_depth = State()


@router.message(StateFilter(None), Command(commands=["step_template"]))
@router.message(WalkerState.first_depth, F.text.lower() == "шаблон презентаций")
async def first_depth_template_find(message: Message, state: FSMContext):
    global indx_list_end
    global indx_list_start
    global dist_indx
    global tree
    await state.clear()
    await state.set_state(WalkerState.first_depth)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=choose_category_template(tree.get_children(tree.get_root())[indx_list_start:indx_list_end], message)
    )
    indx_list_start = indx_list_end
    indx_list_end = indx_list_end + dist_indx

@router.message(Command(commands=["depth_1_template"]))
@router.message(F.text.lower() == "шаблон презентаций")
async def first_depth_template_find(message: Message, state: FSMContext):
    global indx_list_end
    global indx_list_start
    global dist_indx
    global tree
    await state.clear()
    await state.set_state(WalkerState.first_depth)
    await message.answer(
        text="Выберете одну из папок, или выведите все вложенные в эти папки файлы",
        reply_markup=choose_category_template(tree.get_children(tree.get_root())[indx_list_start:indx_list_end], message)
    )
    indx_list_start = indx_list_end
    indx_list_end = indx_list_end + dist_indx

