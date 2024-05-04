from Repo.TGDesignBot.main.DBHandler.insert_scripts import insert_many_fonts, insert_many_images, insert_many_templates, insert_many_users
from Repo.TGDesignBot.main.YandexDisk import YaDiskInfo
from Repo.TGDesignBot.main.YandexDisk import YaDiskHandler

def fill_database(yadisk_info : YaDiskInfo) -> None:
    insert_many_fonts(yadisk_info.get_fonts())
    insert_many_images(yadisk_info.get_images())
    insert_many_templates(yadisk_info.get_templates())
    insert_many_users(['5592902615 admin'])
