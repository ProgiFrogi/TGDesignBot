import json

from TGDesignBot.utility.tg_utility import can_go_right as check_right, download_with_link, \
    send_file_from_local
from TGDesignBot.utility.tg_utility import can_go_left as check_left
from TGDesignBot.utility.tg_utility import update_indx as update_user_indx
from TGDesignBot.DBHandler import (get_fonts_by_template_id,
                                             get_all_tags_by_template_id,
                                             get_slides_by_tags_and_template_id,
                                             get_templates_by_index)
from TGDesignBot.YandexDisk.YaDiskInfo import TemplateInfo
from aiogram import types

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from ..keyboards import main_menu_kb, only_main_menu_button_kb
from ..keyboards.choose_file_keyboard import choose_file_kb, download_file, work_with_tags
from TGDesignBot.pptxHandler import get_template_of_slides, SlideInfo, remove_template
from TGDesignBot.YandexDisk import get_download_link

router = Router()

dist_indx = 1


class WalkerState(StatesGroup):
    # В состоянии храним child_list, indx_list_start\end, can_go_back
    choose_button = State()
    choose_category = State()
    choose_file = State()
    choose_tags = State()


@router.message(WalkerState.choose_file, F.text.lower() == "далее")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

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
            text="Выберите однин из файлов",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(WalkerState.choose_file, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

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
            text="Выберите одну из папок, или выведите все вложенные в эти папки файлы",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(WalkerState.choose_file, F.text.lower() == "получить шрифты")
@router.message(WalkerState.choose_tags, F.text.lower() == "получить шрифты")
async def get_fonts(message: types.Message, state: FSMContext):
    user_info = await state.get_data()
    template_id = user_info["file_id"]
    list_fonts = get_fonts_by_template_id(template_id)
    reply_markup = only_main_menu_button_kb(message)
    if len(list_fonts) == 0:
        await message.answer(
            text="Для данной презентации нет шрифтов!",
            reply_markup=reply_markup
        )
        return

    try:
        await message.answer(
            text="Дождитесь полной отправки шрифтов..."
        )
    except:
        print('Error')
    try:
        path = list_fonts[0][1] + '/' + list_fonts[0][3]
        link = get_download_link(path)
        await download_with_link(message, link, 'fonts.zip')
        reply_markup = main_menu_kb(message)
        await message.answer(
            text="Все шрифты отправлены!",
            reply_markup=reply_markup
        )
    except:
        pass


@router.message(WalkerState.choose_file, F.text.lower() == "как установить шрифты?")
@router.message(WalkerState.choose_tags, F.text.lower() == "как установить шрифты?")
async def send_info(message: types.Message, state: FSMContext):
    try:
        await message.answer(
            text='Дождитесь отправки файла...'
        )
    except:
        print('Proxy error')
    path = './Data/Appdata/00 How to install fonts.pdf'
    await send_file_from_local(message, path, 'How to install fonts.pdf')
    reply_markup = only_main_menu_button_kb(message)
    await message.answer(
        text='Это вам поможет',
        reply_markup=reply_markup
    )


@router.message(WalkerState.choose_tags, F.text.lower() == "далее")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        user_info = await state.get_data()
        user_tags = user_info['user_tags']
        indx_list_end = user_info['indx_list_end']
        list_tags = user_info['list_tags']

        indx_list_start = indx_list_end
        indx_list_end = indx_list_end + dist_indx

        can_go_right = await check_right(indx_list_end, len(list_tags))
        can_go_left = await check_left(indx_list_start)
        reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)
        await message.answer(
            text=f"Введите ваши теги через ';' или Выберите их из предложенных ниже \n Ваши теги: {user_tags}",
            reply_markup=reply_markup
        )
        await update_user_indx(state, indx_list_start, indx_list_end)

@router.message(WalkerState.choose_tags, F.text.lower() == "назад")
async def first_depth_template_find(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']

        user_info = await state.get_data()
        user_tags = user_info['user_tags']
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        list_tags = user_info['list_tags']

        indx_list_start -= dist_indx
        indx_list_end -= dist_indx

        can_go_right = await check_right(indx_list_end, len(list_tags))
        can_go_left = await check_left(indx_list_start)

        reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)
        await message.answer(
            text=f"Введите ваши теги через ';' или Выберите их из предложенных ниже \n Ваши теги: {user_tags}",
            reply_markup=reply_markup
        )

        await update_user_indx(state, indx_list_start, indx_list_end)


@router.message(WalkerState.choose_tags, F.text.lower() == "очистить теги")
async def clear_tags(message: Message, state: FSMContext):
    # Clear user_tags
    await state.update_data(user_tags=[])
    # Default output
    user_info = await state.get_data()
    user_tags = user_info['user_tags']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    list_tags = user_info['list_tags']

    can_go_right = await check_right(indx_list_end, len(list_tags))
    can_go_left = await check_left(indx_list_start)

    reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)
    await message.answer(
        text=f"Введите ваши теги через ';' или Выберите их из предложенных ниже \n Ваши теги: {user_tags}",
        reply_markup=reply_markup
    )


@router.message(WalkerState.choose_tags, F.text.lower() == "найти слайды по введеным тегам")
async def clear_tags(message: Message, state: FSMContext):
    user_info = await state.get_data()
    user_tags = user_info['user_tags']
    template_id = user_info['file_id']

    slides_list = get_slides_by_tags_and_template_id(user_tags, template_id)
    # No need slides
    if (len(slides_list) == 0):
        indx_list_start = user_info['indx_list_start']
        indx_list_end = user_info['indx_list_end']
        list_tags = user_info['list_tags']

        can_go_right = await check_right(indx_list_end, len(list_tags))
        can_go_left = await check_left(indx_list_start)

        reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)

        try:
            await message.answer(
                text=f'Нет слайдов в данной презентации, содержащих следующие теги: \n {user_tags}',
                reply_markup=reply_markup
            )
        except:
            print('error')
    else:
        try:
            await message.answer(
                text='Дождитесь, пока файл загрузится...'
            )
        except:
            print('error2')
        path_to_save = f'./Data/slides/{message.from_user.id}.pptx'
        slide_info = SlideInfo(slides_list[0][0], ';'.join(user_tags))
        for slide in slides_list[1:]:
            slide_info.add_id(slide[0])
        get_template = get_templates_by_index(template_id)
        template = get_template[0]
        template_info = TemplateInfo(template[2], template[1])
        slide_info.add_template_info(template_info)
        get_template_of_slides(path_to_save, slide_info)
        try:
            await send_file_from_local(message, path_to_save, 'Slides.pptx')
        except:
            print('err2')
        reply_markup = download_file(message)
        await message.answer(
            text='Ваш файл успешно загружен!',
            reply_markup=reply_markup
        )
        remove_template(path_to_save)


@router.message(WalkerState.choose_tags)
async def choose_tags(message: Message, state: FSMContext):
    user_info = await state.get_data()
    user_tags = user_info['user_tags']
    indx_list_start = user_info['indx_list_start']
    indx_list_end = user_info['indx_list_end']
    list_tags = user_info['list_tags']
    print(list_tags)

    input_tags = message.text.split(';')
    for tag in input_tags:
        if tag in user_tags:
            await message.answer(
                text=f'Тег "{tag}" уже добавлен'
            )
            continue
        if tag not in list_tags:
            await message.answer(
                text=f'Извините, тега "{tag}" в презентации нет'
            )
        else:
            await message.answer(
                text=f'Тег "{tag}" добавлен'
            )
            user_tags.append(tag)
    can_go_right = await check_right(indx_list_end, len(list_tags))
    can_go_left = await check_left(indx_list_start)
    await state.update_data(user_tags=user_tags)

    reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)
    await message.answer(
        text=f"Введите ваши теги через ';' или Выберите их из предложенных ниже \n Ваши теги: {user_tags}",
        reply_markup=reply_markup
    )


@router.message(WalkerState.choose_file)
async def choose_category(message: Message, state: FSMContext):
    with open("config.json", "r") as file:
        config = json.load(file)
        dist_indx = config['dist']
        user_info = await state.get_data()
        file_name_list = user_info['file_name_list']
        type_file = user_info['type_file']
        if message.text not in file_name_list:
            await message.answer(
                text="Простите, такого файла здесь нет =("
            )
            return

        file_id = None
        link = None
        file_name = None
        file_path = None
        files_list = user_info['files_list']

        for file in files_list:
            if file[2] == message.text:
                file_id = file[0]
                file_path = file[1]
                file_name = file[2]

                await state.update_data(file_id=file_id)
                await state.update_data(link=link)
                await state.update_data(file_path=file_path)
                await state.update_data(file_name=file_name)
                break

        if (type_file == 'template'):
            link = get_download_link(str(file_path) + '/' + str(file_name))
            reply_markup = download_file(message)
            await message.answer(
                text="Ваш файл загружается..."
            )
            await download_with_link(message, link, file_name)
            await message.answer(
                text="Ваш файл успешно загружен!",
                reply_markup=reply_markup
            )

        if (type_file == 'slide'):
            await state.clear()
            await state.set_state(WalkerState.choose_tags)

            list_tags = get_all_tags_by_template_id(file_id)
            try:
                list_tags.remove('')
            except:
                print('No empty tags')
            await state.update_data(list_tags=list_tags)
            await state.update_data()
            await state.update_data(user_tags=[])
            await state.update_data(file_id=file_id)

            indx_list_start = 0
            indx_list_end = indx_list_start + dist_indx
            can_go_right = await check_right(indx_list_end, len(list_tags))
            can_go_left = await check_left(indx_list_start)
            await state.update_data(indx_list_start=indx_list_start)
            await state.update_data(indx_list_end=indx_list_end)

            await update_user_indx(state, indx_list_start, indx_list_end)

            reply_markup = await work_with_tags(list_tags[indx_list_start:indx_list_end], can_go_left, can_go_right, state)
            await message.answer(
                text="Введите ваши теги через ';' или Выберите их из предложенных ниже",
                reply_markup=reply_markup
            )
        if (type_file == 'font'):
            font_name = get_fonts_by_template_id(file_id)
            if (len(font_name) == 0):
                reply_markup = only_main_menu_button_kb(message)
                await message.answer(
                    text="Для данной презентации нет шрифтов!",
                    reply_markup=reply_markup
                )
            link = get_download_link(file_path + '/' + font_name[0][3])
            reply_markup = download_file(message)
            try:
                await message.answer(
                    text="Дождитесь полной отправки шрифтов..."
                )
            except:
                print('Error')
            try:
                await download_with_link(message, link, 'fonts.zip')
                reply_markup = main_menu_kb(message)
                await message.answer(
                    text="Все шрифты отправлены!",
                    reply_markup=reply_markup
                )
            except:
                print('Font send error')
