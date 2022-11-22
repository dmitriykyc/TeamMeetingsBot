from aiogram.dispatcher.filters.state import StatesGroup, State


class GetAnswer(StatesGroup):
    get_text_place = State()
    get_text_people = State()
    end_state = State()
