import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from TGDesignBot.TelegramHandler.handlers import (simple_func_handler, main_menu_handler, admin_menu_handler,
                                                  choose_file, admin_choose_file_for_delete, no_handled)
from TGDesignBot.TelegramHandler.handlers import walker_menu
from asyncscheduler import AsyncScheduler

async def setup_bot_commands(bot: Bot):
    bot_commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/actions", description="Узнать основные функции"),
        BotCommand(command="/help", description="Напишите нам, для решения проблем!")
    ]
    await bot.set_my_commands(bot_commands)



async def pr():
    print('I <3 python!')


# Func for including router and start work
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    # Include router
    dp.include_router(main_menu_handler.router)
    dp.include_router(simple_func_handler.router)
    dp.include_router(admin_menu_handler.router)
    dp.include_router(admin_choose_file_for_delete.router)
    dp.include_router(choose_file.router)
    dp.include_router(walker_menu.router)
    dp.include_router(no_handled.router)
    # Start bot
    await setup_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, ssl=False)
    a = AsyncScheduler()
    await a.start()
    await a.repeat(1, 1, pr)


async def start_bot():
    logging.basicConfig(level=logging.INFO)
    try:
        # Start bot
        await main()
    except:
        print('Exit')


if __name__ == '__main__':
    start_bot()
