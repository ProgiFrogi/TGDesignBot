import json
from TGDesignBot.DBHandler.create_tables import create_tables
from TGDesignBot.DBHandler.fill_database import fill_database
from TGDesignBot.YandexDisk.YaDiskHandler import get_all_files_in_disk
from TGDesignBot.DBHandler.drop_scripts import drop_tables
from TGDesignBot.DBHandler.insert_scripts import insert_many_users


def initialize_database() -> None:
    drop_tables()
    create_tables()
    with open("./admins.json", "r") as admins_file:
        config = json.load(admins_file)

    admins = config["admin_id"]

    if len(admins) != 0:
        insert_many_users(admins)
    fill_database(get_all_files_in_disk())
