from TGDesignBot.DBHandler.create_tables import create_tables
from TGDesignBot.DBHandler.fill_database import fill_database
from TGDesignBot.YandexDisk.YaDiskHandler import get_all_files_in_disk
from TGDesignBot.DBHandler.drop_scripts import drop_tables
from TGDesignBot.DBHandler.insert_scripts import insert_many_users


def initialize_database():
    drop_tables()
    create_tables()
    insert_many_users([[5592902615, 'admin']])
    fill_database(get_all_files_in_disk())
