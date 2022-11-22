from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_rating_choise_date():
    menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Текущий месяц',
                                                             callback_data='this_month')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Общая по всем месяцам',
                                                             callback_data='all_months')
                                    ]
                                ])
    return menu
