import asyncio
import json
import os
import datetime
import pickle

import yadisk
from dotenv import load_dotenv

from TGDesignBot.DBHandler.initialize_database import initialize_database
from TGDesignBot.TelegramHandler import bot as TGbot
from TGDesignBot.Tree.ClassTree import Tree
from TGDesignBot.YandexDisk.YaDiskHandler import update_tree
from TGDesignBot.YandexDisk.UpdateDisk import update_tree_and_db
from apscheduler.schedulers.background import BackgroundScheduler


async def main():
    # Fill database + create tree with dir
    # load_dotenv()
    tree = Tree()
    # update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    # with open("Tree/ObjectTree.pkl", "wb") as fp:
    #     pickle.dump(tree, fp)
    # initialize_database()
    last_updated_time = datetime.datetime.fromisoformat(json.load(open("config.json"))["last-update-time"])
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_tree_and_db, "interval", hours=5, args=[tree, last_updated_time])
    scheduler.start()

    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())
