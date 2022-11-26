import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline_answer_data import data_send_answer
from postgre.commands_db import select_user, create_new_answer, db_done_meeting, add_text_place_to_meeting, \
    add_text_about_user_to_meeting, db_finish_meeting, add_rating, bd_make_free_user, append_image, \
    select_is_active_meeting
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
        user_about = list(select_user(callback_data["user_about"])[0])
        if select_is_active_meeting(call.from_user['id'], user_about[0]):
            await state.set_state(GetAnswer.get_text_place)
            await call.message.delete()
            db_done_meeting(call.from_user['id'], user_about[0])
            await call.message.answer(
                f'🤩Отлично! Рады что вы встретились c {user_about[1]} ( {user_about[2]} ) и классно поболтали. \n\n'
                '✏️Опишите Ваши впечатления о <b>МЕСТЕ</b>, в котором Вы встречались, отправьте это сообщение прямо в чат👇\n\n'
                'Можно добавить одно фото и текст')
            user_id = call.from_user['id']
            await state.update_data(from_user=user_id, user_about=user_about, photo=[])
        else:
            await call.message.edit_text('Ваша встреча уже завершена ранее или не состоялась.')

    @dp.message_handler(content_types=['photo', 'text'], state=GetAnswer.get_text_place)
    async def answer_place(message: types.Message, state: FSMContext):
        data_photo = await state.get_data()
        photo = data_photo['photo']
        if 'photo' in message:
            append_image(message.photo[-1]['file_id'])
            text = message.caption
            photo.append(message.photo[0]['file_id'])
            await state.update_data(photo=photo)
        else:
            text = message.text
        if text:
            await message.answer('Отлично! '
                                 '\n✏️Теперь поделитесь впечатлениями о <b>собеседнике</b> и отправьте сообщение в этот чат👇\n\n'
                                 'Можно добавить одно фото и текст')
            state_data = await state.get_data()
            user_about = state_data['user_about']
            add_text_place_to_meeting(message.from_user['id'], user_about[0], text=text)
            await state.update_data(txt_about_place=text)
            await state.set_state(GetAnswer.get_text_people)

    @dp.message_handler(content_types=['photo', 'text'], state=GetAnswer.get_text_people)
    async def next_answer(message: types.Message, state: FSMContext):
        data_photo = await state.get_data()
        photo = data_photo['photo']
        if 'photo' in message:
            text = message.caption  # Если нет текста вернет None
            append_image(message.photo[-1]['file_id'])
            photo.append(message.photo[0]['file_id'])
            await state.update_data(photo=photo)
        else:
            text = message.text
        if text:
            await state.update_data(txt_about_people=text)
            data = await state.get_data()
            about_user = data['user_about']
            add_text_about_user_to_meeting(message.from_user['id'], about_user[0], text=text)
            db_finish_meeting(message.from_user['id'], about_user[0])
            await message.answer(
                '👍Прекрасно! Спасибо!\nКогда вам будет назначена новая встреча, сюда придет приглашение.')
            await state.finish()
            add_rating(message.from_user["id"])
            bd_make_free_user(message.from_user["id"])

            create_answer_xlsx(data['from_user'], data['user_about'][0], data['txt_about_place'],
                               data['txt_about_people'])
            logging.info(f'{message.from_user["first_name"]} ( {message.from_user["username"]})'
                         f' написал обратную свзь о {data["user_about"][1]} ( {data["user_about"][2]} )\n\n'
                         f'Текст о месте: \n'
                         f'{data["txt_about_place"]}'
                         f'\nТекст о человеке:\n'
                         f'{data["txt_about_people"]}')

            for admin in admins:
                photos = data['photo']
                media = types.MediaGroup()
                if photos:
                    for ph in photos:
                        media.attach_photo(ph)
                    await dp.bot.send_media_group(admin, media)
                await dp.bot.send_message(admin,
                                          f'{message.from_user["first_name"]} ( {message.from_user["username"]} )'
                                          f' написал обратную свзь о {data["user_about"][1]}'
                                          f' ( {data["user_about"][2]} )\n\n'
                                          f'Текст о месте: \n'
                                          f'{data["txt_about_place"]}'
                                          f'\nТекст о человеке:\n'
                                          f'{data["txt_about_people"]}')

    @dp.message_handler()
    async def answ_unicnown(message: types.Message):
        logging.info(f'Пользователь {message.from_user}\n'
                     f'Написал неизвестный текст:\n'
                     f'{message.text}')
        await message.answer('К сожалению, я пока не знаю такой команды🙃')
