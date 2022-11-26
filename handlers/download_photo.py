import calendar
import datetime
from datetime import date
from time import sleep

from aiogram import Dispatcher, types
import zipfile
import os

from aiogram.types import CallbackQuery

from keyboards.inline_download_photo import inline_download_photo
from postgre.commands_db import select_all_photos


def register_download_photo_handler(dp: Dispatcher):
    @dp.message_handler(text='Скачать архив с фото')
    async def downl_rar(message: types.Message):
        await message.answer('За какой период хотите скачать фотографии?', reply_markup=inline_download_photo())

    @dp.callback_query_handler(text=['download_this_month', 'download_previous_months'])
    async def downl_this_month(call: CallbackQuery):
        print(call.data)
        await call.answer()
        year_now = date.today().strftime('%Y')

        if call.data == 'download_this_month':
            month_now = int(date.today().strftime('%m'))
            get_last_day_month = calendar.monthrange(int(year_now), int(month_now))[1]
            start_month = date.today().replace(day=1)
            end_month = date.today().replace(day=int(get_last_day_month))
        else:
            first_day__month = date.today().replace(day=1)
            previous_month = first_day__month - datetime.timedelta(days=1)
            str_previous_month = previous_month.strftime('%m')
            str_previous_year = previous_month.strftime("%Y")
            get_last_day_month = calendar.monthrange(int(str_previous_year), int(str_previous_month))[1]
            start_month = datetime.datetime.strptime(f'01-{str_previous_month}-{str_previous_year}', '%d-%m-%Y').date()
            end_month = datetime.datetime.strptime(f'{get_last_day_month}-'
                                                   f'{str_previous_month}-'
                                                   f'{str_previous_year} 23:59:999999',
                                                   '%d-%m-%Y %H:%M:%f')
        all_photos = select_all_photos(start_month, end_month)
        zip_name = f"{date.today().strftime('%d-%m-%Y')}.zip"
        if all_photos:
            await call.message.answer('Я соберу фотографии и отправлю в чат по готовности')
            for ph in all_photos:
                file_2 = await dp.bot.get_file(ph[1])
                await dp.bot.download_file(file_2.file_path, f'{ph[0]}.jpg')
                z = zipfile.ZipFile(zip_name, "a", zipfile.ZIP_DEFLATED)
                z.write(f"{ph[0]}.jpg")
                z.close()
                if os.path.isfile(f"{ph[0]}.jpg"):
                    os.remove(f"{ph[0]}.jpg")

                sleep(0.5)

            await call.message.answer_document(open(zip_name, 'rb'), caption='Вот Ваш архив')
            if os.path.isfile(zip_name):
                os.remove(zip_name)
        else:
            await call.message.answer('Фотографий за этот период нет.')