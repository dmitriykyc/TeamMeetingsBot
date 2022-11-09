import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline_answer_data import data_send_answer
from postgre.commands_db import select_user, create_new_answer
from soft.create_xlsx import create_answer_xlsx
from state.answer_state import GetAnswer
from filters.all_admins import get_all_admins

admins = get_all_admins()
logging.basicConfig(level=logging.INFO, filename="TMBot_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s:-->")


def register_answer_form_handler(dp: Dispatcher):
    @dp.callback_query_handler(data_send_answer.filter(), state='*')
    async def start_answer(call: CallbackQuery, callback_data, state: FSMContext):
        await call.answer()
        await state.set_state(GetAnswer.get_text)
        user_aboute = list(select_user(callback_data["user_aboute"])[0])
        await call.message.answer(
            f'🤩Отлично! Рады что вы встретились c {user_aboute[1]} (@{user_aboute[2]}) и классно поболтали, '
            'опишите Ваши впечатления(в одном сообщении) о собеседнике и отправьте в бот это сообщение👇')
        user_id = call.from_user['id']
        await state.update_data(from_user=user_id, user_aboute=user_aboute)

    @dp.message_handler(state=GetAnswer.get_text)
    async def next_answer(message: types.Message, state: FSMContext):
        await message.answer('👍Прекрасно! Спасибо!')
        await state.update_data(text=message.text)
        data = await state.get_data()
        await state.finish()
        user_aboute = data['user_aboute']
        text = message.text
        create_new_answer(data['from_user'], data['user_aboute'][0], text)
        create_answer_xlsx(data['from_user'], data['user_aboute'][0], text)
        logging.info(f'{message.from_user["first_name"]} (@{message.from_user["username"]})'
                     f' написал обратную свзь о {user_aboute[1]} (@{user_aboute[2]})\n\n'
                     f'Текст: \n'
                     f'{text}')

        for admin in admins:
            await dp.bot.send_message(admin, f'{message.from_user["first_name"]} (@{message.from_user["username"]})'
                                             f' написал обратную свзь о {user_aboute[1]} (@{user_aboute[2]})\n\n'
                                             f'Текст: \n'
                                             f'{text}')

        @dp.message_handler()
        async def answ_unicnown(nessage: types.Message):
            logging.info(f'Пользователь {message.from_user}\n'
                         f'Написал неизвестный текст:\n'
                         f'{message.text}')
            await nessage.answer('К сожалению, я пока не знаю такой команды🙃')
