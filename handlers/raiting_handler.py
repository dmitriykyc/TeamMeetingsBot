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
    @dp.callback_query_handler(data_rating.filter())
    async def create_rating(call: CallbackQuery, callback_data):
        await call.answer()
        print(callback_data)
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
            my_rait = 'Ваш рейтинг:\n'
            my_rait2 = 'У вас пока нет рейтинга.'
            result_text = 'Баллы суммируются за количество встреч по всем месяцам и за оценки участников ' \
                          '(голосование в конце месяца). \n\n' \
                          'Топ-10 за все месяцы:\n\n'
            for pos, us_rat in enumerate(final_result, 1):
                user = select_user(us_rat[0])[0]
                result_text += f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} баллов \n'
                if user[0] == call.from_user['id']:
                    my_rait2 = f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} баллов'
            await call.message.answer(result_text)
            await call.message.answer(my_rait + my_rait2)
        else:
            await call.answer('Пока статистика пуста, попробуйте позже.')

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
            my_rait = 'Ваш рейтинг:\n'
            my_rait2 = 'У вас пока нет рейтинга.'
            result_text = 'Баллы суммируются за количество встреч в месяц и за оценки участников ' \
                          '(голосование в конце месяца). \n\n' \
                          'Топ-10 за текущий месяц:\n\n'
            for pos, us_rat in enumerate(final_result, 1):
                user = select_user(us_rat[0])[0]
                result_text += f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} баллов \n'
                if user[0] == call.from_user['id']:
                    my_rait2 = f'{pos}. {user[1]} ( {user[2]} ) - {us_rat[1]} баллов'
            await call.message.answer(result_text)
            await call.message.answer(my_rait + my_rait2)
        else:
            await call.answer('Пока статистика пуста, попробуйте позже.')
