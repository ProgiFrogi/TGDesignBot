import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from Repo.TGDesignBot.main.TelegramHandler.handlers import simple_func_handler, main_menu_handler, walker_menu, \
    admin_menu_handler, choose_file


# Func for including router and start work
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    # Include router
    dp.include_router(main_menu_handler.router)
    dp.include_router(admin_menu_handler.router)
    dp.include_router(simple_func_handler.router)
    dp.include_router(walker_menu.router)
    dp.include_router(choose_file.router)
    # Start bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, ssl=False)


async def start_bot():
    logging.basicConfig(level=logging.INFO)
    try:
        # Start bot
        await main()
    except:
        print('Exit')


if __name__ == '__main__':
    start_bot()
