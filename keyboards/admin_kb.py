from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# keyboard admin
keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

load_button = KeyboardButton('Загрузить')
menu_button = KeyboardButton('Показать весь список')

keyboard_admin.add(load_button, menu_button)

# keyboard cancel machine
keyboard_admin_cancel_machine = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton('Остановить загрузку'))

# keyboard input add machine
keyboard_admin_database = InlineKeyboardMarkup(row_width=1)

inline_button_chemical = InlineKeyboardButton(text='🧪 Агрохимикаты', callback_data='Admin show catalog chemical')
inline_button_devices = InlineKeyboardButton(text='📟 Агроприборы', callback_data='Admin show catalog devices')
inline_button_fertilizers = InlineKeyboardButton(text='🪵 Удобрения', callback_data='Admin show catalog fertilizers')
inline_button_seeds = InlineKeyboardButton(text='🌱 Семена и растения', callback_data='Admin show catalog seeds')

keyboard_admin_database.add(inline_button_chemical, inline_button_devices, inline_button_fertilizers, inline_button_seeds)

# keyboard input delete item machine
keyboard_admin_delete_db = InlineKeyboardMarkup(row_width=1)

del_inline_button_chemical = InlineKeyboardButton(text='🧪 Агрохимикаты', callback_data='Admin catalog del from chemical')
del_inline_button_devices = InlineKeyboardButton(text='📟 Агроприборы', callback_data='Admin catalog del from devices')
del_inline_button_fertilizers = InlineKeyboardButton(text='🪵 Удобрения', callback_data='Admin catalog del from fertilizers')
del_inline_button_seeds = InlineKeyboardButton(text='🌱 Семена и растения', callback_data='Admin catalog del from seeds')

keyboard_admin_delete_db.add(del_inline_button_chemical, del_inline_button_devices, del_inline_button_fertilizers, del_inline_button_seeds)
