from aiogram.fsm.state import default_state, StatesGroup, State
# from Repo.TGDesignBot.main.DBHandler import get_templates_from_directory, get_templates_from_child_directories

async def can_go_right(indx_list_end : int, len_child_list : int) -> bool:
    return indx_list_end < len_child_list


async def can_go_left(indx_list_start : int) -> bool:
    return indx_list_start != 0

async def can_go_back(user_data) -> bool:
    return not (len(user_data) == 0 or user_data[-1] == "Шаблон презентаций")

async def update_data(state : State, path, indx_list_start, indx_list_end, can_go_back, child_list) -> None:
    await state.update_data(path=path)
    await state.update_data(can_go_back=can_go_back)
    await state.update_data(child_list=child_list)
    await update_indx(state, indx_list_start, indx_list_end)

async def update_indx(state : State, indx_list_start, indx_list_end) -> None:
    await state.update_data(indx_list_start=indx_list_start)
    await state.update_data(indx_list_end=indx_list_end)

# async def get_list_of_files(state : State) -> list:
#     user_info = await state.get_data()
#     list_of_path = user_info['path']
#
#     list_of_files = []
#     if (list_of_path[0] == "Шаблоны презентаций"):
#         list_of_files = ['3']