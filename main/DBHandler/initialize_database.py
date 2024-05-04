import yadisk
from Repo.TGDesignBot.main.DBHandler.create_tables import create_tables
from Repo.TGDesignBot.main.DBHandler.fill_database import fill_database
from Repo.TGDesignBot.main.YandexDisk.YaDiskHandler import update_tree, get_all_files_in_disk
import os
from dotenv import load_dotenv
import pickle
import json
from datetime import datetime
from Repo.TGDesignBot.main.Tree import ClassTree as ClassTree

tree = pickle.load(open("Tree/ObjectTree.pkl", "rb"))

def initialize_database():
    create_tables()
    #
    # load_dotenv()
    # disk = yadisk.YaDisk(token='y0_AgAAAAB0mCJzAAu2ugAAAAEDmpiEAABS62wojd1JzLOgYt13FLWLWa_5uQ')
    # with open('config.json') as file:
    #     last_update_time = json.load(file)['last-update-time']
    #     update_tree(tree, datetime.fromisoformat(last_update_time))
    fill_database(get_all_files_in_disk())