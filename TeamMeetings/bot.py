import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from TeamMeetings.handlers.answer_from_user import register_answer_form_handler
from TeamMeetings.handlers.create_daiting_handler import create_dating_handler
from TeamMeetings.handlers.start_handler import register_start_handlers


def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    pass



def register_all_handlers(dp):
    register_start_handlers(dp)
    create_dating_handler(dp)
    register_answer_form_handler(dp)



async def main():
    bot = Bot(token='5748588465:AAEIz1tmCGWG1cZjp9-4A7YEdWfWnID5H_c', parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
        print("Bot started")
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
