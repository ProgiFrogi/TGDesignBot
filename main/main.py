import asyncio
import pickle
import TelegramHandler.bot as TGbot
from Repo.TGDesignBot.main.DBHandler.initialize_database import initialize_database

async def main():
    await TGbot.start_bot()

if __name__ == '__main__':

    initialize_database()
    asyncio.run(main())