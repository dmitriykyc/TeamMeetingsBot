from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.types.chat_member import ChatMember

from TeamMeetings.keyboards.reply_main import reply_main_menu
from TeamMeetings.postgre.commands_db import add_user, select_user, update_active_user

admins = [354585871, 485696536]


def register_start_handlers(dp: Dispatcher):
    @dp.message_handler(commands='start')
    async def get_start(message: types.Message):
        user_id = message.from_user['id']
        first_name = message.from_user['first_name']
        username = message.from_user['username']
        user_db = select_user(user_id)
        if user_db == []:
            add_user(user_id, first_name, username)
        if user_db != [] and user_db[0][3] == False:
            update_active_user(user_id)

        if message.from_user['id'] in admins:
            await message.answer('Привет, Админ!✌️\n'
                                 'У тебя есть кнопки, которых нет у других пользователей, ты '
                                 'можешь запустить рандомайзер и скачать отчет с результатами\n\n'
                                 'Так же в сообщениях мы будем отправлять обратную связь от'
                                 'сотрудников после встречи. \n\n'
                                 'Если меню с кнопками спряталось, нажми: 🎛, рядом с кнопкой микрофона.',
                                 reply_markup=reply_main_menu)
        else:
            await message.answer(f'Привет, {message.from_user["first_name"]}✌️\n'
                                 f'Это бот встреч между сотрудникми нашей команды.\n'
                                 f'Мы будем случайным образом выбирать двух сотрудников и вам нужно встретиться, далее'
                                 f' писать обратную связь по собеседникм сюда. \nВам придёт уведомление.')

    @dp.my_chat_member_handler(run_task=True)
    async def some_handler(my_chat_member: types.ChatMemberUpdated):
        '''Обрабатывает выход пользователя из чата'''
        user_id = my_chat_member['chat']['id']
        if my_chat_member['new_chat_member']['status'] == "kicked":
            update_active_user(user_id)

    @dp.message_handler(text='Отчет Exel')
    async def get_report(message: types.Message):
        if message.from_user['id'] in admins:
            await message.answer('Таблица со всеми ответами участников:')
            doc = open("/Users/dmitriykyc/PycharmProjects/TeamMeetingsBot/TeamMeetings/soft/Report_Bot.xlsx", "rb")
            await message.answer_document(doc)


        else:
            await message.answer('Функция доступна только для администраторов')
