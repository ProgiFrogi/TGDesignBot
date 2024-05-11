from Repo.TGDesignBot.main.utility.tg_utility import can_go_right as check_right
from Repo.TGDesignBot.main.utility.tg_utility import can_go_left as check_left
from Repo.TGDesignBot.main.utility.tg_utility import update_indx as update_user_indx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from ..keyboards.choose_file_keyboard import choose_file_kb

router = Router()

dist_indx = 1


class AdminState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back
    choose_button = State()
    choose_category = State()
    choose_file = State()


@router.message(AdminState.choose_file, F.text.lower() == "следующий блок")
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
    reply_markup = await choose_file_kb(file_name_list[indx_list_start:indx_list_end], message, can_go_left,
                                        can_go_right)
    await message.answer(
        text="Выберете один из файлов",
        reply_markup=reply_markup
    )

    await update_user_indx(state, indx_list_start, indx_list_end)
