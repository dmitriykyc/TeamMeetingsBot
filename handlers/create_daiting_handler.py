import logging
import random

from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from keyboards.inline_answer import inline_confirm_admin, inline_confirm_user, inline_send_answer
from keyboards.inline_answer_data import data_confirm_admin, data_confirm_user
from postgre.commands_db import select_all_active_users, select_user
from filters.all_admins import get_all_admins

admins = get_all_admins()
logging.basicConfig(level=logging.INFO, filename="TMBot_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s:-->")


def create_dating_handler(dp: Dispatcher):
    def change_two_users():
        all_users = select_all_active_users()
        rand_user_1 = random.choice(all_users)
        rand_user_2 = random.choice(all_users)
        return rand_user_1, rand_user_2

    @dp.message_handler(text='Запустить рандомайзер')
    async def start_random(message: types.Message):
        get_users = change_two_users()
        while get_users[0] == get_users[1]:
            get_users = change_two_users()
        user_1 = list(get_users[0])
        user_2 = list(get_users[1])

        text = f'Рандомно выбранные пользователи для встречи:\n' \
               f'👤{user_1[1]} (@{user_1[2]})\n' \
               f'👤{user_2[1]} (@{user_2[2]})\n\n' \
               f'Отправляем приглашение?'
        print(user_1)
        print(user_2)
        await message.answer(f'{text}', reply_markup=inline_confirm_admin(user_1[0], user_2[0]))

    @dp.callback_query_handler(data_confirm_admin.filter())
    async def send_invite(call: CallbackQuery, callback_data):
        await call.answer()
        print(callback_data)
        print(call)
        user1 = list(select_user(callback_data['user1'])[0])
        user2 = list(select_user(callback_data['user2'])[0])
        print(user1)
        logging.info(f'Отправлены приглашения для: \n'
                     f'{user1}\n'
                     f'{user2}')
        await call.message.answer('✅Отлично!\n '
                                  'Приглашения отправлены, вы получите подтверждения от этих пользователей.')
        await dp.bot.send_message(user1[0],
                                  f'🎉Вы были выбраны для встречи с {user2[1]} (@{user2[2]})! Пожалуйста, подтвердите ваше участие',
                                  reply_markup=inline_confirm_user(user1[0], user2[0]))
        await dp.bot.send_message(user2[0],
                                  f'🎉Вы были выбраны для встречи с {user1[1]} (@{user1[2]})! Пожалуйста, подтвердите ваше участие',
                                  reply_markup=inline_confirm_user(user2[0], user1[0]))

    @dp.callback_query_handler(data_confirm_user.filter())
    async def done_from_user(call: CallbackQuery, callback_data):
        await call.answer()
        user_from = call.from_user
        user_aboute = list(select_user(callback_data['user_aboute'])[0])
        logging.info(f'{call.from_user["first_name"]} (@{user_from["username"]}) подтвердил встречу '
                     f'c {user_aboute[1]} (@{user_aboute[2]})')
        await call.message.edit_text(f'👍Отлично! \n'
                                     f'После вашей встречи с {user_aboute[1]} (@{user_aboute[2]})'
                                     f'нажмите кнопку внизу',
                                     reply_markup=inline_send_answer(user_from['id'], user_aboute[0]))

        text = f'✨{call.from_user["first_name"]} (@{user_from["username"]}) подтвердил встречу' \
               f' c {user_aboute[1]} (@{user_aboute[2]})'

        for admin in admins:
            await dp.bot.send_message(admin, text)