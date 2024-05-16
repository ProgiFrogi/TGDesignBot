import asyncio
import os
import datetime
import pickle

import yadisk
from dotenv import load_dotenv

from Repo.TGDesignBot.main.DBHandler.initialize_database import initialize_database
from Repo.TGDesignBot.main.TelegramHandler import bot as TGbot
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
from Repo.TGDesignBot.main.YandexDisk.YaDiskHandler import update_tree


async def main():
    # Fill database + create tree with dir
    load_dotenv()
    # tree = Tree()
    # update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    # with open("Tree/ObjectTree.pkl", "wb") as fp:
    #     pickle.dump(tree, fp)
    # initialize_database()
    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())
