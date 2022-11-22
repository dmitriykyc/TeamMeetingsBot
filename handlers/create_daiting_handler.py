import logging
import random

from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from keyboards.inline_answer import inline_confirm_admin, inline_confirm_user, inline_send_answer, inline_agreed_meeting
from keyboards.inline_answer_data import data_confirm_admin, data_confirm_user, data_agreed_meeting
from postgre.commands_db import select_all_active_users, select_user, add_tabl_meetings, \
    db_confirm_meeting, select_all_active_and_free_users, bd_make_busy_user, select_one_meeting_confirm_or_not, \
    select_is_free_user
from filters.all_admins import get_all_admins

admins = get_all_admins()
logging.basicConfig(level=logging.INFO, filename="TMBot_log.log", filemode="r+",
                    format="%(asctime)s %(levelname)s %(message)s:-->")


def create_dating_handler(dp: Dispatcher):
    def change_two_users():
        all_users = select_all_active_and_free_users()
        if len(all_users) < 2:
            return None
        else:
            rand_user_1 = random.choice(all_users)
            all_users.remove(rand_user_1)
            rand_user_2 = random.choice(all_users)
            return rand_user_1, rand_user_2

    @dp.message_handler(text='Запустить рандомайзер')
    async def start_random(message: types.Message):
        get_users = change_two_users()
        if get_users:
            user_1 = list(get_users[0])
            user_2 = list(get_users[1])
            text = f'Рандомно выбранные пользователи для встречи:\n' \
                   f'👤{user_1[1]} ({user_1[2]})\n' \
                   f'👤{user_2[1]} ({user_2[2]})\n\n' \
                   f'Отправляем приглашение?'
            print(user_1)
            print(user_2)
            await message.answer(f'{text}', reply_markup=inline_confirm_admin(user_1[0], user_2[0]))
        else:
            await message.answer('Не удалось собрать пару, подождите пока кто то освободится.')

    @dp.callback_query_handler(data_confirm_admin.filter())
    async def send_invite(call: CallbackQuery, callback_data):
        await call.answer()
        user1 = list(select_user(callback_data['user1'])[0])
        user2 = list(select_user(callback_data['user2'])[0])
        # Дополнительные проверки активности от прошлых сообщений
        is_active_1 = select_is_free_user(user1[0])
        is_active_2 = select_is_free_user(user2[0])
        if is_active_1 and is_active_2:
            add_tabl_meetings(user1[0], user2[0])
            add_tabl_meetings(user2[0], user1[0])
            bd_make_busy_user(user1[0])
            bd_make_busy_user(user2[0])
            await dp.bot.send_message(user1[0],
                                      f'🎉Вы были выбраны для встречи с {user2[1]} ( {user2[2]} )!\n'
                                      f'У вас есть 7 дней чтобы договориться, выбрать место и время. \n'
                                      f'Если встреча не будет подтверждена, она аннулируется.\n\n'
                                      f'Когда договоритесь, нажмите на кнопку под этим сообщением 👇',
                                      reply_markup=inline_confirm_user(user1[0], user2[0]))
            await dp.bot.send_message(user2[0],
                                      f'🎉Вы были выбраны для встречи с {user1[1]} ( {user1[2]} )!'
                                      f'У вас есть 7 дней чтобы договориться, выбрать место и время. \n'
                                      f'Если встреча не будет подтверждена, она аннулируется.\n\n'
                                      f'Когда договоритесь, нажмите на кнопку под этим сообщением 👇',
                                      reply_markup=inline_confirm_user(user2[0], user1[0]))
            logging.info(f'Отправлены приглашения для: \n'
                         f'{user1}\n'
                         f'{user2}')
            await call.message.delete()
            await call.message.answer('✅Отлично!\n '
                                      'Приглашения отправлены, вы получите подтверждения от этих пользователей.')
        else:
            await call.message.delete()
            await call.message.answer(f'Пользователь/ли уже заняты встречей')


    @dp.callback_query_handler(data_confirm_user.filter())
    async def done_from_user(call: CallbackQuery, callback_data):
        await call.answer()
        print(11111111)
        user_from = call.from_user
        user_about = list(select_user(callback_data['user_about'])[0])
        already_confirm = select_one_meeting_confirm_or_not(user_from['id'], user_about[0])
        print(already_confirm)
        if already_confirm and already_confirm[0][0] == False:
            db_confirm_meeting(user_from['id'], user_about[0])
            logging.info(f'{call.from_user["first_name"]} ( {user_from["username"]} ) договорились о встрече '
                         f'c {user_about[1]} ({user_about[2]})')

            await call.message.delete()
            await call.message.answer(f'👍Отлично! \n Теперь у Вас есть 7 дней для того чтобы завершить Вашу встречу. '
                                      f'После вашей встречи с {user_about[1]} ( {user_about[2]} ) '
                                      f'нажмите кнопку внизу',
                                      reply_markup=inline_send_answer(user_from['id'], user_about[0]))

            text = f'⚡️Подтверждение встречи:\n' \
                   f'{call.from_user["first_name"]} ( {user_from["username"]} ) договорились о встрече ' \
                   f'c {user_about[1]} ({user_about[2]})'

            for admin in admins:
                await dp.bot.send_message(admin, text)
        else:
            await call.message.edit_text('Вы уже договорились ранее')


    # @dp.callback_query_handler(data_agreed_meeting.filter())
    # async def agreed_meeting(call: CallbackQuery, callback_data):
    #     await call.answer()
    #     user_from = call.from_user
    #     user_about = list(select_user(callback_data['user_about'])[0])
    #     db_confirm_meeting(user_from['id'], user_about[0])
    #     await call.message.edit_text(f'👍Отлично! \n'
    #                                  f'После вашей встречи с {user_about[1]} ({user_about[2]})'
    #                                  f'нажмите кнопку внизу',
    #                                  reply_markup=inline_send_answer(user_from['id'], user_about[0]))
    #     text = f'🤝Договорились о встрече:\n' \
    #            f'{call.from_user["first_name"]} ({user_from["username"]})\n договорился о встрече с  ' \
    #            f'{user_about[1]} ({user_about[2]}).\n' \
    #            f'Я отправлю уведомление, после того, как получу обратную связь.'
    #
    #     for admin in admins:
    #         await dp.bot.send_message(admin, text)
