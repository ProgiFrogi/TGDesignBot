import copy
import datetime
import yadisk
from Repo.TGDesignBot.main.DBHandler.select_scripts import get_template_id_by_name
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
from Repo.TGDesignBot.main.YandexDisk.YaDiskInfo import YaDiskInfo
from Repo.TGDesignBot.main.DBHandler.fill_database import fill_database
from Repo.TGDesignBot.main.DBHandler.delete_scripts import delete_template
from Repo.TGDesignBot.main.pptxHandler import remove_template
from dotenv import load_dotenv

from .YaDiskInfo import TemplateInfo

load_dotenv()
ya_disk = yadisk.YaDisk(token=('y0_AgAAAAB0mCJzAAu2ugAAAAEDmpiEAABS62wojd1JzLOgYt13FLWLWa_5uQ'))


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


# Recursive find in YaDisk. Takes the current directory and find files in it.
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
                ya_disk_info.add_template(item.name, item.path[: item.path.rfind('/')])

            elif is_font(item):
                ya_disk_info.add_font(item.path[: item.path.rfind('/')])


# Function take an empty lists ant trying to bring from YDisc all files created from last
# checking. Using ISO 8601 format of time with milliseconds.
def get_last_added_files(last_updated_time: datetime.datetime, ya_disk_info: YaDiskInfo):
    check_token(ya_disk)
    try:
        __search_in_directory__('/', last_updated_time, ya_disk_info)
    except Exception as e:
        ya_disk_info.clear()
        raise Exception("Can't find any files")


# Recursive find deleted templates from last update in trash box of YaDisk.
# Takes the current directory and find files in it.
def __get_templates_from_trash__(directory: str,
                                 last_updated_time: datetime.datetime,
                                 ya_disk_info: YaDiskInfo):
    for item in ya_disk.trash_listdir(directory):
        if item.is_dir() and (not is_images(item)) and (not is_graphics(item)):
            __get_templates_from_trash__(item.path, last_updated_time, ya_disk_info)

        elif last_updated_time < item.deleted and is_template(item):
            ya_disk_info.add_template(item.name, item.path[: item.path.rfind('/')])


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


# Update actuality of the current tree object.
def update_tree(tree: Tree, last_updated_time):
    check_token(ya_disk)
    __delete_nodes__('/', tree)
    __add_nodes__('/', last_updated_time, tree)
    last_updated_time = datetime.datetime.now(tz=datetime.timezone.utc)


# This function returns all files from YDisk.
# Returns an object of class YaDiskInfo.
def get_all_files_in_disk() -> YaDiskInfo:
    last_updated_time = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    ya_disk_info = YaDiskInfo()
    get_last_added_files(last_updated_time, ya_disk_info)
    return ya_disk_info


# Upload a local file to YaDisk by dest_path.
def upload_to_disk(dest_path: list, local_path: str):
    check_token(ya_disk)
    path_to_files = list(ya_disk.listdir('/'))[0].path
    dest_path_str = path_to_files[:path_to_files.rfind('/') + 1] + '/'.join(dest_path) + '/' + local_path.split('/')[-1]
    ya_disk.upload(local_path, dest_path_str)


def get_download_link(path: str) -> str:
    check_token(ya_disk)
    return ya_disk.get_download_link(path)


# Update actuality of database. Insert new files and removing deleted templates.
def update_db(last_updated_time: datetime.datetime):
    ya_disk_info = YaDiskInfo()
    get_last_added_files(last_updated_time, ya_disk_info)
    fill_database(ya_disk_info)
    ya_disk_info.clear()
    __get_templates_from_trash__('/', last_updated_time, ya_disk_info)
    for template_info in ya_disk_info.templates:
        template_id = get_template_id_by_name(template_info.path, template_info.name)
        delete_template(template_id)


# Update actuality of database and tree.
def update_tree_and_db(tree: Tree, last_updated_time: datetime.datetime):
    time_copy = copy.deepcopy(last_updated_time)
    update_tree(tree, last_updated_time)
    update_db(time_copy)


# Delete file (not directory) from YaDisk.
def delete_from_disk(path: str):
    check_token(ya_disk)
    try:
        if path.endswith('.pptx'):
            remove_template('./Data/Templates/' + path[path.rfind('/') + 1:])
            template_info = TemplateInfo(path[path.rfind('/') + 1:], path[:path.rfind('/')])
            template_id = get_template_id_by_name(template_info.path, template_info.name)
            delete_template(template_id)
        ya_disk.delete(path)
    except Exception as e:
        raise "No such file or directory"
