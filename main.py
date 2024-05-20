import asyncio
import os
import datetime
import pickle

import yadisk
from dotenv import load_dotenv

from TGDesignBot.DBHandler.initialize_database import initialize_database
from TGDesignBot.TelegramHandler import bot as TGbot
from TGDesignBot.Tree.ClassTree import Tree
from TGDesignBot.YandexDisk.YaDiskHandler import update_tree


async def main():
    # Fill database + create tree with dir
    load_dotenv()
    tree = Tree()
    update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    with open("Tree/ObjectTree.pkl", "wb") as fp:
        pickle.dump(tree, fp)
    initialize_database()
    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())
