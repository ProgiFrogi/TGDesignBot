import datetime
import yadisk
from . import YaDiskInfo
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_STR = str(os.getenv('YANDEX_DISK_TOKEN'))
print(f'Your token: ' + ('*' * 56) + f'{TOKEN_STR[-5:]}')
ya_disk = yadisk.YaDisk(token=str(os.getenv('YANDEX_DISK_TOKEN')))


# Takes item from YaDisk and checking is it a photo directory.
def is_images(item) -> bool:
    return item.is_dir() and ('фото' in item.name.lower() or "photo" in item.name.lower())


# Takes item from YaDisk and checking is it a graphics directory.
def is_graphics(item) -> bool:
    return item.is_dir() and ('график' in item.name.lower() or "graphic" in item.name.lower())


# Takes item from YaDisk and checking is it a template.
def is_template(item) -> bool:
    return item.name.endswith('.pptx')


# Takes item from YaDisk and checking is it a font.
def is_font(item) -> bool:
    return item.name.endswith('.zip') and ('шрифт' in item.name.lower() or "font" in item.name.lower())


# Checking is token valid.
def check_token(token):
    if not token.check_token():
        raise Exception("Invalid token")


# Recursive find in YDisk. Takes the current directory and find files in it.
def __search_in_directory__(directory: str,
                            last_updated_time: datetime.datetime,
                            ya_disk_info: YaDiskInfo):
    for item in ya_disk.listdir(directory):
        if item.is_dir() and (not is_images(item)) and (not is_graphics(item)):
            __search_in_directory__(item.path, last_updated_time, ya_disk_info)

        elif last_updated_time < item.created:
            if is_images(item) or is_graphics(item):
                ya_disk_info.add_image(item.path, item.path[: item.path.rfind('/')])

            elif is_template(item):
                ya_disk_info.add_template(item.name, item.file, item.path[: item.path.rfind('/')])

            elif is_font(item):
                ya_disk_info.add_font(item.file, item.path[: item.path.rfind('/')])


# Function take an empty lists ant trying to bring from YDisc all files created from last
# checking. Using ISO 8601 format of time with milliseconds.
def get_last_added_files(last_updated_time: datetime.datetime, ya_disk_info: YaDiskInfo):
    check_token(ya_disk)
    try:
        __search_in_directory__('/', last_updated_time, ya_disk_info)
    except Exception as e:
        ya_disk_info.clear()
        raise Exception("Can't find any files")


# Removes outdated information from the folder tree.
def __delete_nodes__(directory: str, tree: Tree):
    for item in ya_disk.trash_listdir(directory):
        if item.is_dir():
            __delete_nodes__(item.path, tree)
            tree.delete_node(item.name)


# Adds information about new directories to the tree.
def __add_nodes__(directory: str, last_updated_time, tree: Tree):
    for item in ya_disk.listdir(directory):
        if item.is_dir() and (not is_images(item)) and (not is_font(item)):
            if last_updated_time < item.created:
                if directory == "/":
                    tree.insert("root", item.name)
                else:
                    tree.insert(directory[directory.rfind('/') + 1:], item.name)
            __add_nodes__(item.path, last_updated_time, tree)


def update_tree(tree: Tree, last_updated_time):
    check_token(ya_disk)
    __delete_nodes__('/', tree)
    __add_nodes__('/', last_updated_time, tree)
    last_updated_time = datetime.datetime.now(tz=datetime.timezone.utc)


# This function returns all files from YDisk.
# Returns an object of class YaDiskInfo.
def get_all_files_in_disk() -> YaDiskInfo:
    last_updated_time = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    ya_disk_info = YaDiskInfo.YaDiskInfo()
    get_last_added_files(last_updated_time, ya_disk_info)
    return ya_disk_info


# Upload a local file to YaDisk by dest_path.
def upload_to_disk(dest_path: list, local_path: str):
    check_token(ya_disk)
    path_to_files = list(ya_disk.listdir('/'))[0].path
    dest_path_str = path_to_files[:path_to_files.rfind('/') + 1] + '/'.join(dest_path) + '/' + local_path.split('/')[-1]
    ya_disk.upload(local_path, dest_path_str)
