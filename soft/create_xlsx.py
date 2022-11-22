import datetime
import os

import openpyxl
from openpyxl.styles import Alignment

from postgre.commands_db import select_user

path = os.getenv("PATH_XLSX")

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

def create_answer_xlsx(from_user, about_user, txt_about_place, txt_about_user):
    from_user_data = select_user(from_user)[0]
    about_user_data = select_user(about_user)[0]
    print(from_user_data)

    workbook = openpyxl.load_workbook(path)
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
    sheet[f'D{max_row}'] = txt_about_place
    sheet[f'E{max_row}'].alignment = long_text
    sheet[f'E{max_row}'] = txt_about_user

    workbook.save(path)


