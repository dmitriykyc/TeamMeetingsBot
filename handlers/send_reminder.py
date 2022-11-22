import asyncio

import aioschedule
import calendar
from datetime import date

from keyboards.inline_answer import inline_confirm_user, inline_rating, inline_send_answer
from postgre.commands_db import select_active_meetings, db_deactivate_meeting, db_change_day, select_user, \
    select_all_result_meet_month, select_result_meet_month_for_user, bd_make_free_user, \
    select_active_meeting_after_confirmed


async def get_last_day(dp, get_last_day_month):
    start_month = date.today().replace(day=1)
    end_month = date.today().replace(day=int(get_last_day_month))
    all_act_meet = select_all_result_meet_month(start_month, end_month)
    print(all_act_meet)
    done_user = []
    for meet in all_act_meet:
        user_id = meet[1]
        if user_id not in done_user:
            all_meet_for_user = select_result_meet_month_for_user(user_id, start_month, end_month)
            print(all_meet_for_user)
            companions = []
            for end_meet in all_meet_for_user:
                companion = select_user(end_meet[2])
                if companion and companion[0] not in companions:
                    companions.append(companion[0])

            await dp.bot.send_message(user_id, '📈Собираем рейтинг в конце меяца. '
                                               'Кто из собеседников Вам понравился больше всего?'
                                               ' Кому добавим ещё один балл?',
                                      reply_markup=inline_rating(user_id, companions))
            done_user.append(user_id)

async def send_seven_days(dp):
    all_meetings = select_active_meetings()

    if all_meetings:
        print('Metiing is not confirmed')
        for meeting in all_meetings:
            user = select_user(meeting[1])[0]
            user_about = select_user(meeting[2])[0]

            if meeting[5] == 1:
                db_deactivate_meeting(meeting[0])
                bd_make_free_user(user[0])
                bd_make_free_user(user_about[0])
                await dp.bot.send_message(meeting[1], f'К сожалению мы отменили Вашу встречу'
                                                      f' c {user_about[1]} ( {user_about[2]} ).')
            else:
                new_day = meeting[5] - 1
                db_change_day(meeting[0], new_day)
                await dp.bot.send_message(meeting[1], f'Вы еще не подтвердили встречу c'
                                                      f' {user_about[1]} ( {user_about[2]} ), осталось {new_day} дней!',
                                                      reply_markup=inline_confirm_user(user[0], user_about[0]))
        await asyncio.sleep(1)
    # Отправляем напоминания чтобы встретились
    all_meetings_bef_conf = select_active_meeting_after_confirmed()
    if all_meetings_bef_conf:
        print('visit is not end')
        for meeting_conf in all_meetings_bef_conf:
            user = select_user(meeting_conf[1])[0]
            user_about = select_user(meeting_conf[2])[0]

            if meeting_conf[5] == 1:
                db_deactivate_meeting(meeting_conf[0])
                bd_make_free_user(user[0])
                bd_make_free_user(user_about[0])
                await dp.bot.send_message(meeting_conf[1], f'К сожалению, вы не успели встретиться,'
                                                           f' мы аннулировали Вашу встречу с '
                                                           f'{user_about[1]} ( {user_about[2]} ).')
            else:
                new_day = meeting_conf[5] - 1
                db_change_day(meeting_conf[0], new_day)
                await dp.bot.send_message(meeting_conf[1], f'Вы еще не сходили на встречу с'
                                                      f' {user_about[1]} ( {user_about[2]} ), осталось {new_day} дней! '
                                                           f'По истечению дней, встреча аннулируется!',
                                                      reply_markup=inline_send_answer(user[0], user_about[0]))
        await asyncio.sleep(1)

    year_now = date.today().strftime('%Y')
    month_now = date.today().strftime('%m')
    day_now = int(date.today().strftime('%d'))
    get_last_day_month = calendar.monthrange(int(year_now), int(month_now))[1]

    # if get_last_day_month == int(day_now):
    if 29 == int(day_now):
        await get_last_day(dp, get_last_day_month)


async def start_remimber(dp):
    print('Start remimber1')
    aioschedule.every().day.at("10:00").do(send_seven_days, dp)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


