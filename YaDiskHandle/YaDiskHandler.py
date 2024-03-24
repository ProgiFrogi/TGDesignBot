import datetime

import yadisk

ya_disk = yadisk.YaDisk(token=Token)


# Recursive find in YDisk. Takes the current directory and find files in it.
def __search_in_directory__(directory: str,
                            last_updated_time: datetime.datetime,
                            templates: list,
                            fonts: list,
                            images: list):
    for item in ya_disk.listdir(directory):
        if item.is_dir() and not ('фото' in item.name.lower() or "photo" in item.name.lower()):
            __search_in_directory__(item.path,
                                    last_updated_time,
                                    templates,
                                    fonts,
                                    images)

        if item.is_dir and ('фото' in item.name.lower() or "photo" in item.name.lower()):
            images.append({'position': item.path,
                           'path': item.path[: item.path.rfind('/')]})

        elif last_updated_time < item.created:
            if item.name.endswith('.pptx'):
                templates.append({'name': item.name,
                                  'file': item.file,
                                  'path': item.path[: item.path.rfind('/')]})

            elif item.name.endswith('.zip'):
                fonts.append({'file': item.file,
                              'path': item.path[: item.path.rfind('/')]})


# Function take an empty lists ant trying to bring from YDisc all files created from last
# checking. Using ISO 8601 format of time with milliseconds.
# Writing into templates dictionary by keys:
#            'name' - the name of file
#            'file' - the download link of file
#            'path' - the path of file from root to last directory
# Writing into fonts dictionary by keys:
#            'file' - the download link of file
#            'path' - the path of file from root to last directory
# Writing into images dictionary by keys:
#            'position' - the current path of file. Can easily access to this file.
#            'path' - the path of file from root to last directory.
def __get_last_added_files__(last_updated_time: datetime.datetime,
                             templates: list,
                             fonts: list,
                             images: list):
    if not ya_disk.check_token():
        raise Exception("Invalid token")

    try:
        __search_in_directory__('/', last_updated_time, templates, fonts, images)
    except Exception as e:
        templates.clear()
        fonts.clear()
        images.clear()
        raise Exception("Can't find any files")


# This function returns all files from YDisk.
# Returns templates, fonts, images of uploaded in this order
def get_all_files_in_disk() -> [list, list, list]:
    last_updated_time = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    templates = []
    fonts = []
    images = []
    __get_last_added_files__(last_updated_time, templates, fonts, images)
    return templates, fonts, images
