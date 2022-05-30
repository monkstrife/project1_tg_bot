from typing import Text
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client, keyboard_client_catalog
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

# func start working
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'<b>Здравствуйте! Вас приветствует AgrosegmentBot!</b>', parse_mode='html', reply_markup=keyboard_client)
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting contact details
async def get_contact(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Режим работы: пн-сб <u>с 7:00 до 18:00</u></b>\n<b>Адрес: <u>ул. Авилова</u></b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting contact details
async def get_inforamation(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>. . . ИНФОРМАЦИЯ О КОМПАНИИ . . .</b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting catalog
async def get_catalog(message: types.Message):
    await bot.send_message(message.from_user.id, '<b><u>🛎ВЫБЕРИТЕ РАЗДЕЛ🛎</u></b>', parse_mode='html', reply_markup=keyboard_client_catalog)
    if(message.from_user.id != message.chat.id):
        await message.delete()

async def get_menu(callback: types.CallbackQuery):
    read = await sqlite_db.sql_read(callback.data.replace("Client catalog ", ""))
    for item in read:
        await callback.message.answer(f'{item[0]}\n{item[1]}\n{item[2]}\n{item[3]}')

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(get_contact, Text(equals='☎️ Контакты ☎️', ignore_case=True))
    dp.register_message_handler(get_inforamation, Text(equals='🔎 О компании 🔍', ignore_case=True))
    dp.register_message_handler(get_catalog, Text(equals='🗂 Каталог 🗂', ignore_case=True))
    dp.register_callback_query_handler(get_menu, lambda x: x.data and x.data.startswith('Client catalog '))
