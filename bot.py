import asyncio
import os
import logging

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers.answer_from_user import register_answer_form_handler
from handlers.create_daiting_handler import create_dating_handler
from handlers.download_photo import register_download_photo_handler
from handlers.raiting_handler import register_rating_handler
from handlers.send_reminder import start_remimber
from handlers.start_handler import register_start_handlers

load_dotenv()
logging.basicConfig(level=logging.INFO, filename="TMBot_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s:-->")



def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_download_photo_handler(dp)
    register_rating_handler(dp)
    register_start_handlers(dp)
    create_dating_handler(dp)
    register_answer_form_handler(dp)


async def main():
    bot = Bot(token=os.getenv("TOKEN"), parse_mode='HTML')

    dp = Dispatcher(bot, storage=RedisStorage2(host=os.getenv('REDIS_HOST')))
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    asyncio.create_task(start_remimber(dp))

    # start
    try:
        print("Bot started")
        logging.info('Bot srarted')
        await dp.start_polling()
        print('123')
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
