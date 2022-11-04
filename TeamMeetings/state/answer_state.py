from aiogram.dispatcher.filters.state import StatesGroup, State


class GetAnswer(StatesGroup):
    get_text = State()
    end_state = State()
