from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_download_photo():
    menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Текущий месяц',
                                                             callback_data='download_this_month')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Прошлый месяц',
                                                             callback_data='download_previous_months')
                                    ]
                                ])
    return menu
