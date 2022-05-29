from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

load_button = KeyboardButton('Загрузить')
cancel_button = KeyboardButton('Остановить')
menu_button = KeyboardButton('Показать весь список')

keyboard_admin.add(load_button, cancel_button, menu_button)
