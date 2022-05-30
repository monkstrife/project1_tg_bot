from cgitb import text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button_contact = KeyboardButton('☎️ Контакты ☎️')
button_inforamation = KeyboardButton('🔎 О компании 🔍')
button_catalog = KeyboardButton('🗂 Каталог 🗂')
keyboard_client.row(button_contact, button_inforamation).add(button_catalog)

keyboard_client_catalog = InlineKeyboardMarkup(row_width=1)
inline_button_chemical = InlineKeyboardButton(text='🧪 Агрохимикаты', callback_data='Client catalog chemical')
inline_button_devices = InlineKeyboardButton(text='📟 Агроприборы', callback_data='Client catalog devices')
inline_button_fertilizers = InlineKeyboardButton(text='🪵 Удобрения', callback_data='Client catalog fertilizers')
inline_button_seeds = InlineKeyboardButton(text='🌱 Семена и растения', callback_data='Client catalog seeds')
keyboard_client_catalog.add(inline_button_chemical, inline_button_devices, inline_button_fertilizers, inline_button_seeds)
