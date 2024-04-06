import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from .handlers import simple_func_handler, main_menu_handler, walker_menu


#
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    # Подключение роутеров
    dp.include_router(main_menu_handler.router)
    dp.include_router(simple_func_handler.router)
    dp.include_router(walker_menu.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def start_bot():
    logging.basicConfig(level=logging.INFO)
    try:
        # Запуск бота
        await main()
    except:
        await print('Exit')

if __name__ == '__main__':
    # Запуск логирования
    logging.basicConfig(level=logging.INFO)
    try:
    #Запуск бота
        asyncio.run(main())
    except:
        print('Exit')