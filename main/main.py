import asyncio
import pickle
import TelegramHandler.bot as TGbot
from Repo.TGDesignBot.main.DBHandler.initialize_database import initialize_database
from Repo.TGDesignBot.main.Tree.ClassTree import Tree
import Repo.TGDesignBot.main.YandexDisk.YaDiskHandler as Ydhandler
import datetime

async def main():
    tree = Tree()
    Ydhandler.update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))

    with open("Tree/ObjectTree.pkl", "wb") as fp:
        pickle.dump(tree, fp)
    initialize_database()
    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())