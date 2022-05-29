from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
button_work_schedule = KeyboardButton('Режим работы')
button_address = KeyboardButton('Адрес')
button_menu = KeyboardButton('Меню')
keyboard_client.add(button_work_schedule, button_address, button_menu)
