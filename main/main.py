import asyncio
import pickle
import TelegramHandler.bot as TGbot

async def main():
    await TGbot.start_bot()

if __name__ == '__main__':
    asyncio.run(main())