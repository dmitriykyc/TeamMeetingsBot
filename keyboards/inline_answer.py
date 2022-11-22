from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_answer_data import data_confirm_admin, data_confirm_user, data_send_answer, data_agreed_meeting, \
    data_rating


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


def inline_confirm_user(user_from, user_about):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='🤝Мы договорились',
                                                             callback_data=data_confirm_user.new(
                                                                 user_from=user_from,
                                                                 user_about=user_about
                                                             ))
                                    ]
                                ])
    return menu


def inline_agreed_meeting(user_from, user_about):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='🤝Мы договориись о встрече',
                                                             callback_data=data_agreed_meeting.new(
                                                                 user_from=user_from,
                                                                 user_about=user_about
                                                             ))
                                    ]
                                ])
    return menu


def inline_send_answer(user_from, user_about):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='✅Нажать после встречи',
                                                             callback_data=data_send_answer.new(
                                                                 user_from=user_from,
                                                                 user_about=user_about
                                                             ))
                                    ]
                                ])
    return menu


def inline_rating(user_from, companions):
    print(companions)
    print('*****')
    for el in companions:
        print(1)
        print(el)
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=f"{ell[1]} - ({ell[2]})",
                                                             callback_data=data_rating.new(
                                                                 user_from=user_from,
                                                                 user_about=ell[0]
                                                             ))
                                    ] for ell in companions
                                ])
    print(menu)
    return menu
