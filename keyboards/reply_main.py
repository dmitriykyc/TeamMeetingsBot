from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запустить рандомайзер')
        ],
        [
            KeyboardButton(text='Отчет Exele')
        ],
        [
            KeyboardButton(text='Скачать архив с фото')
        ]
    ], resize_keyboard=True
)
