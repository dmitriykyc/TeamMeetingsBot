import asyncio
import logging
import aioschedule
import calendar
from datetime import date
from aiogram.utils.exceptions import BotBlocked

from keyboards.inline_answer import inline_confirm_user, inline_rating, inline_send_answer
from postgre.commands_db import select_active_meetings, db_deactivate_meeting, db_change_day, select_user, \
    select_all_result_meet_month, select_result_meet_month_for_user, bd_make_free_user, \
    select_active_meeting_after_confirmed, bd_is_free_user


def plural_days(n):
    days = ['день', 'дня', 'дней']

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2
    return days[p]


async def get_last_day(dp, get_last_day_month):
    start_month = date.today().replace(day=1)
    end_month = date.today().replace(day=int(get_last_day_month))
    all_act_meet = select_all_result_meet_month(start_month, end_month)
    done_user = []
    for meet in all_act_meet:
        user_id = meet[1]
        if user_id not in done_user:
            all_meet_for_user = select_result_meet_month_for_user(user_id, start_month, end_month)
            companions = []
            for end_meet in all_meet_for_user:
                companion = select_user(end_meet[2])
                if companion and companion[0] not in companions:
                    companions.append(companion[0])
            logging.info('Пробуем разослать опрос в конце месяца')
            try:
                await dp.bot.send_message(user_id, '📈Собираем рейтинг в конце меяца.\n '
                                                   'Кто из собеседников Вам понравился больше всего?'
                                                   ' Кому добавим ещё один балл?',
                                          reply_markup=inline_rating(user_id, companions))
                logging.info('Успешно')
            except BotBlocked as BotB:
                logging.info(f'ERROR BOT CODE - {str(BotB)}\n Что то тут произошло с '
                             f'пользователем при рассылке опроса в конце месяца: {user_id}')
            done_user.append(user_id)
        await asyncio.sleep(1)


async def send_seven_days(dp):
    logging.info('Начинаем рассылку send_seven_days')
    all_meetings = select_active_meetings()
    if all_meetings:
        for meeting in all_meetings:
            user = select_user(meeting[1])[0]
            user_about = select_user(meeting[2])[0]

            if meeting[5] == 1:
                db_deactivate_meeting(meeting[0])
                bd_make_free_user(user[0])
                bd_make_free_user(user_about[0])

                # Проверка, можно ли написать человеку:
                free_user_now = bd_is_free_user(meeting[1])
                logging.info(f'Пробуем написать от отмене пользователю(69 стр) --> {user}')
                if free_user_now[0][0]:
                    try:
                        await dp.bot.send_message(meeting[1], f'К сожалению, мы отменили Вашу встречу'
                                                              f' c {user_about[1]} ( {user_about[2]} ).')
                        logging.info('Успешно')
                    except BotBlocked:
                        logging.info(f'{meeting} - f{meeting[1]} что то случилось с пользователем,'
                                     f' не можем отправить сообщение!')
                else:
                    logging.info(f'{meeting} - {meeting[1]} Покинул бота')
            else:
                new_day = meeting[5] - 1
                db_change_day(meeting[0], new_day)

                # Проверка, можно ли написать человеку:
                free_user_now = bd_is_free_user(meeting[1])
                logging.info(f'Пробуем написать пользователю(86 стр) --> {user}')
                if free_user_now[0][0]:
                    try:
                        await dp.bot.send_message(meeting[1], f'Вы еще не подтвердили встречу c'
                                                              f' {user_about[1]} ( {user_about[2]} ), осталось {new_day} {plural_days(new_day)}!',
                                                  reply_markup=inline_confirm_user(user[0], user_about[0]))
                        logging.info('Успешно')
                    except BotBlocked:
                        logging.info(f'{meeting} - f{meeting[1]} что то случилось с пользователем,'
                                     f' не можем отправить сообщение!')
                else:
                    logging.info(f'{meeting} - f{meeting[1]} Покинул бота')
            await asyncio.sleep(1)
    # Отправляем напоминания чтобы встретились
    all_meetings_bef_conf = select_active_meeting_after_confirmed()
    if all_meetings_bef_conf:
        logging.info(f'Начинаем рассылку для тех, кто договорился но не встретился')
        for meeting_conf in all_meetings_bef_conf:
            user = select_user(meeting_conf[1])[0]
            user_about = select_user(meeting_conf[2])[0]

            if meeting_conf[5] == 1:
                db_deactivate_meeting(meeting_conf[0])
                bd_make_free_user(user[0])
                bd_make_free_user(user_about[0])

                # Проверка, можно ли написать человеку:
                free_user_now = bd_is_free_user(meeting_conf[1])
                logging.info(f'Пробуем написать об отмене встречи (114 стр) --> {user}')
                if free_user_now[0][0]:
                    try:
                        await dp.bot.send_message(meeting_conf[1], f'К сожалению, мы отменили вашу встречу c '
                                                                   f'{user_about[1]} ( {user_about[2]} ).')
                        logging.info('Успешно')
                    except BotBlocked:
                        logging.info(f'{meeting_conf} - f{meeting_conf[1]} что то случилось с пользователем,'
                                     f' не можем отправить сообщение!')
                else:
                    logging.info(f'{meeting_conf} - f{meeting_conf[1]} Покинул бота')
            else:
                new_day = meeting_conf[5] - 1
                db_change_day(meeting_conf[0], new_day)
                # Проверка, можно ли написать человеку:
                free_user_now = bd_is_free_user(meeting_conf[1])
                logging.info(f'Пробуем написать пользователю(130 стр) --> {user}')
                if free_user_now[0][0]:
                    try:
                        await dp.bot.send_message(meeting_conf[1], f'Вы еще не сходили на встречу с'
                                                                   f' {user_about[1]} ( {user_about[2]} ), осталось {new_day} {plural_days(new_day)}! '
                                                                   f'По истечению {new_day} {plural_days(new_day)}, встреча аннулируется!',
                                                  reply_markup=inline_send_answer(user[0], user_about[0]))
                        logging.info('Успешно')
                    except BotBlocked:
                        logging.info(f'{meeting_conf} - f{meeting_conf[1]} что то случилось с пользователем,'
                                     f' не можем отправить сообщение!')

                else:
                    logging.info(f'{meeting_conf} - f{meeting_conf[1]} Покинул бота')
            await asyncio.sleep(1)

    year_now = date.today().strftime('%Y')
    month_now = date.today().strftime('%m')
    day_now = int(date.today().strftime('%d'))
    get_last_day_month = calendar.monthrange(int(year_now), int(month_now))[1]

    # if 28 == int(day_now):
    if get_last_day_month == int(day_now):
        await get_last_day(dp, get_last_day_month)

async def start_remimber(dp):
    aioschedule.every().day.at("8:00").do(send_seven_days, dp)
    # aioschedule.every(15).seconds.do(send_seven_days, dp)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
