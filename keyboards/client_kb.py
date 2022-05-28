import telebot
from telebot import types

keyboard_client = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
button_work_schedule = types.KeyboardButton('Режим работы')
button_address = types.KeyboardButton('Адрес')
keyboard_client.add(button_work_schedule, button_address)
