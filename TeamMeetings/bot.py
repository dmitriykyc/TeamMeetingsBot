import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.answer_from_user import register_answer_form_handler
from handlers.create_daiting_handler import create_dating_handler
from handlers.start_handler import register_start_handlers



def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    pass



def register_all_handlers(dp):
    register_start_handlers(dp)
    create_dating_handler(dp)
    register_answer_form_handler(dp)



async def main():
    bot = Bot(token='', parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        print("Bot started")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
