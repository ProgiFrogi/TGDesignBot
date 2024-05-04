from Repo.TGDesignBot.main.DBHandler.create_tables import create_tables
from Repo.TGDesignBot.main.DBHandler.fill_database import fill_database
from Repo.TGDesignBot.main.YandexDisk.YaDiskHandler import update_tree, get_all_files_in_disk


def initialize_database():
    create_tables()
    fill_database(get_all_files_in_disk())
