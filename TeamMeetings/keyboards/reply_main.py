from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запустить рандомайзер')
        ],
        [
            KeyboardButton(text='Отчет Exel')
        ]
    ], resize_keyboard=True
)
