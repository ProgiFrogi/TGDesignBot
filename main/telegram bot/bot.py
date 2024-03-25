import asyncio
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import simple_func_handler, main_menu_handler


#
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    # Подключение роутеров
    dp.include_router(main_menu_handler.router)
    dp.include_router(simple_func_handler.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск логирования
    logging.basicConfig(level=logging.INFO)
    # try:
        #Запуск бота
    asyncio.run(main())
    # except:
    #     print('Exit')