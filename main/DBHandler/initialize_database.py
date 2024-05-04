import yadisk
from Repo.TGDesignBot.main.DBHandler.create_tables import create_tables
from Repo.TGDesignBot.main.DBHandler.fill_database import fill_database
from Repo.TGDesignBot.main.YandexDisk.YaDiskHandler import update_tree, get_all_files_in_disk
from Repo.TGDesignBot.main.DBHandler.drop_scripts import drop_tables
import os
from dotenv import load_dotenv
import pickle
import json
from datetime import datetime
from Repo.TGDesignBot.main.Tree import ClassTree as ClassTree

def initialize_database():
    drop_tables()
    create_tables()
    fill_database(get_all_files_in_disk())