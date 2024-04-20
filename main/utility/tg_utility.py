

async def can_go_right(indx_list_end : int, len_child_list : int) -> bool:
    return indx_list_end < len_child_list


async def can_go_left(indx_list_start : int) -> bool:
    return indx_list_start != 0

async def can_go_back(user_data) -> bool:
    return not (len(user_data) == 0 or user_data[-1] == "Шаблон презентаций")