import os
import logging

from aiogram import Dispatcher, types

from keyboards.reply_main import reply_main_menu
from postgre.commands_db import add_user, select_user, update_active_user, create_table_users, create_table_answers, \
    create_table_meetings, create_table_rating, create_table_images
from filters.all_admins import get_all_admins

admins = get_all_admins()
logging.basicConfig(level=logging.INFO, filename="TMBot_log.log", filemode="r+",
                    format="%(asctime)s %(levelname)s %(message)s:-->")


def register_start_handlers(dp: Dispatcher):

    @dp.message_handler(text='Создай таблицы')
    async def crete_t(message: types.Message):
        create_table_users()
        create_table_answers()
        create_table_meetings()
        create_table_rating()
        create_table_images()

        logging.info('Создали все таблицы')
        await message.answer('Tables is create')

    @dp.message_handler(commands='start')
    async def get_start(message: types.Message):
        user_id = message.from_user['id']
        first_name = message.from_user['first_name']
        if message.from_user['username'] == None:
            username = f'tg://user?id={message.from_user["id"]}'
        else:
            username = '@' + message.from_user['username']
        user_db = select_user(user_id)
        if user_db == []:
            add_user(user_id, first_name, username)
        if user_db != [] and user_db[0][3] == False:
            update_active_user(user_id)
        logging.info(f'Пользователь нажал START: {message.from_user}')

        if message.from_user['id'] in admins:
            await message.answer('Привет, Админ!✌️\n'
                                 'У тебя есть кнопки, которых нет у других пользователей,'
                                 ' ты можешь запустить рандомайзер и скачать отчет с результатами. \n\n'
                                 'Так же в сообщениях мы будем отправлять обратную связь от сотрудников после встречи. \n\n'
                                 'Если меню с кнопками спряталось, нажми: 🎛, рядом с кнопкой микрофона.',
                                 reply_markup=reply_main_menu)
        else:
            await message.answer(f'Привет, {message.from_user["first_name"]}✌️\n'
                                 f'Это бот для встреч сотрудников команды Bazar Family. '
                                 f'\n\nОн будет случайным образом выбирать двух сотрудников, которым предстоит узнать'
                                 f' друг друга поближе, а затем поделиться впечатлениями о собеседнике и '
                                 f'месте встречи.')

    @dp.my_chat_member_handler(run_task=True)
    async def some_handler(my_chat_member: types.ChatMemberUpdated):
        '''Обрабатывает выход пользователя из чата'''
        user_id = my_chat_member['chat']['id']
        if my_chat_member['new_chat_member']['status'] == "kicked":
            update_active_user(user_id)

    @dp.message_handler(text='Отчет Exele')
    async def get_report(message: types.Message):
        logging.info(f'{message.from_user} запросил таблицу для скачивания')
        if message.from_user['id'] in admins:
            await message.answer('Таблица со всеми ответами участников:')
            doc = open(os.getenv("PATH_XLSX"), "rb")
            await message.answer_document(doc)
        else:
            await message.answer('Функция доступна только для администраторов.')

    @dp.message_handler(text='Скрой меня')
    async def sec_me(message: types.Message):
        if message.from_user["id"] == 354585871:
            update_active_user(354585871)
            await message.answer('Ok, Done')
        else:
            await message.answer('Простите, не понимаю о чем Вы.')

