from typing import Optional

from aiogram.utils.callback_data import CallbackData

data_confirm_admin = CallbackData('touch_done_invite', 'user1', 'user2')
data_confirm_user = CallbackData('touch_done_invite_user', 'user_from', 'user_about')
data_send_answer = CallbackData('data_send_answer', 'user_from', 'user_about')
data_agreed_meeting = CallbackData('agreed_meeting', 'user_from', 'user_about')
data_rating = CallbackData('riting', 'user_from', 'user_about')

