from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_answer_data import data_confirm_admin, data_confirm_user, data_send_answer


def inline_confirm_admin(user1, user2):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='✅Подтвердить',
                                                             callback_data=data_confirm_admin.new(
                                                                 user1=user1,
                                                                 user2=user2,
                                                             ))
                                    ]
                                ])
    return menu


def inline_confirm_user(user_from, user_aboute):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='✅Подтвердить',
                                                             callback_data=data_confirm_user.new(
                                                                 user_from=user_from,
                                                                 user_aboute=user_aboute
                                                             ))
                                    ]
                                ])
    return menu


def inline_send_answer(user_from, user_aboute):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='✅Нажать после встречи',
                                                             callback_data=data_send_answer.new(
                                                                 user_from=user_from,
                                                                 user_aboute=user_aboute
                                                             ))
                                    ]
                                ])
    return menu