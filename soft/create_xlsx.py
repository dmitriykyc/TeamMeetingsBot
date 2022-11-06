import datetime

import openpyxl
from openpyxl.styles import Alignment

from postgre.commands_db import select_user

long_text = Alignment(
    horizontal='left',
    vertical='top',
    wrap_text=True,
    shrink_to_fit=True
)
small_text = Alignment(
    horizontal='left',
    vertical='top',
    wrap_text=True,
    shrink_to_fit=True
)

def create_answer_xlsx(from_user, about_user, text):
    from_user_data = select_user(from_user)[0]
    about_user_data = select_user(about_user)[0]
    print(from_user_data)

    workbook = openpyxl.load_workbook('/soft/Report_Bot.xlsx')
    sheet = workbook.active
    max_row = sheet.max_row + 1
    date = datetime.date.today()
    print(date.strftime('%d.%m.%y'))
    sheet[f'A{max_row}'].alignment = long_text
    sheet[f'A{max_row}'] = date
    sheet[f'B{max_row}'].alignment = long_text
    sheet[f'B{max_row}'] = f'{from_user_data[1]} - (@{from_user_data[2]})'
    sheet[f'C{max_row}'].alignment = long_text
    sheet[f'C{max_row}'] = f'{about_user_data[1]} - (@{about_user_data[2]})'
    sheet[f'D{max_row}'].alignment = long_text
    sheet[f'D{max_row}'] = text

    workbook.save('/Users/dmitriykyc/PycharmProjects/TeamMeetingsBot/TeamMeetings/soft/Report_Bot.xlsx')


