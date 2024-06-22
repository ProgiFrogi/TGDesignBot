import asyncio
import datetime
import pickle

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from TGDesignBot.DBHandler.initialize_database import initialize_database
from TGDesignBot.TelegramHandler import bot as TGbot
from TGDesignBot.Tree.ClassTree import Tree
from TGDesignBot.YandexDisk.UpdateDisk import update_tree_and_db
from TGDesignBot.YandexDisk.YaDiskHandler import update_tree


async def main():
    # Fill database + create tree with dir
    load_dotenv()
    tree = Tree()
    update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    with open("./Tree/ObjectTree.pkl", "wb") as fp:
        pickle.dump(tree, fp)
    # Initialize DataBase.
    initialize_database()

    # AutoUpdating information from YaDisk every 5 hours.
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_tree_and_db, "interval", hours=5)
    scheduler.start()

    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())
