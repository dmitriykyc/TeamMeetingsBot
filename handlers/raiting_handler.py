import datetime

from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery
from collections import Counter
from datetime import date
import calendar

from keyboards.inline_answer_data import data_rating
from keyboards.inline_rating import inline_rating_choise_date
from postgre.commands_db import add_rating, select_stat_rating_users, select_user, select_all_stat_rating_users


def register_rating_handler(dp: Dispatcher):
    def plural_ball(n):
        balls = ['балл', 'балла', 'баллов']

        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2
        return balls[p]

    @dp.callback_query_handler(data_rating.filter())
    async def create_rating(call: CallbackQuery, callback_data):
        await call.answer()
        add_rating(callback_data['user_about'], call.from_user['id'])
        await call.message.edit_text('Отлично! Спасибо! Статистику можно посмотреть выполнив команду: /rating')

    @dp.message_handler(commands='rating')
    async def get_rating(message: types.Message):
        await message.answer('Выберите период', reply_markup=inline_rating_choise_date())

    @dp.callback_query_handler(text='all_months')
    async def get_rating_all(call: CallbackQuery):
        await call.answer()
        all_ratings = select_all_stat_rating_users()
        if all_ratings:
            result = Counter(all_ratings)
            final_result = result.most_common()
            my_rait = '<b>Ваш рейтинг:</b>\n'
            my_rait2 = 'У вас пока нет рейтинга. \n\n<b>Рейтинг можно заработать:</b>\n' \
                       '🤝Посещая встречи (+1 балл).\n' \
                       '🗳В конце месяца, будет голосование, на котором можно отдать +1 балл за наиболее интересного собеседника'
            result_text = 'Баллы суммируются за количество встреч в месяц и за оценки участников  ' \
                          '(голосование в конце месяца). \n\n' \
                          '<b>Топ-10 за все месяцы:</b>\n\n'
            for pos, us_rat in enumerate(final_result, 1):
                user = select_user(us_rat[0])[0]
                result_text += f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} {plural_ball(int(us_rat[1]))} \n'
                if user[0] == call.from_user['id']:
                    my_rait2 = f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} {plural_ball(int(us_rat[1]))}'
            await call.message.answer(my_rait + my_rait2)
            await call.message.answer(result_text)
        else:
            await call.message.answer('Пока статистика пуста, попробуйте позже.')

    @dp.callback_query_handler(text='this_month')
    async def get_rating_all(call: CallbackQuery):
        await call.answer()
        year_now = date.today().strftime('%Y')
        month_now = date.today().strftime('%m')
        get_last_day_month = calendar.monthrange(int(year_now), int(month_now))[1]
        start_month = date.today().replace(day=1)
        end_month = datetime.datetime.strptime(f'{get_last_day_month}-'
                                               f'{month_now}-'
                                               f'{year_now} 23:59:999999',
                                               '%d-%m-%Y %H:%M:%f')

        all_ratings = select_stat_rating_users(start_month, end_month)
        if all_ratings:
            result = Counter(all_ratings)
            final_result = result.most_common()
            my_rait = '<b>Ваш рейтинг:</b>\n'
            my_rait2 = 'У вас пока нет рейтинга. \n\n<b>Рейтинг можно заработать:</b>\n' \
                       '🤝Посещая встречи (+1 балл).\n' \
                       '🗳В конце месяца, будет голосование, на котором можно отдать +1 балл за наиболее интересного собеседника'
            result_text = 'Баллы суммируются за количество встреч в месяц и за оценки участников ' \
                          '(голосование в конце месяца). \n\n' \
                          '<b>Топ-10 за текущий месяц:</b>\n\n'
            for pos, us_rat in enumerate(final_result, 1):
                user = select_user(us_rat[0])[0]
                result_text += f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} {plural_ball(int(us_rat[1]))} \n'
                if user[0] == call.from_user['id']:
                    my_rait2 = f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} {plural_ball(int(us_rat[1]))}'
            await call.message.answer(my_rait + my_rait2)
            await call.message.answer(result_text)
        else:
            await call.message.answer('Пока статистика пуста, попробуйте позже.')
