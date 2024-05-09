import asyncio
from Repo.TGDesignBot.main.TelegramHandler import bot as TGbot


async def main():
    # Fill database + create tree with dir
#     tree = Tree()
#     Ydhandler.update_tree(tree, datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
#     with open("Tree/ObjectTree.pkl", "wb") as fp:
#         pickle.dump(tree, fp)
#     initialize_database()
    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())