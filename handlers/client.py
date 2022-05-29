from typing import Text
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

# func start working
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'<b>Здравствуйте</b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        await message.delete()
        await bot.send_message(message.chat.id, f'<b><u>{message.from_user.first_name}</u>, напишите боту в ЛС.\n@AgroSegmentBot</b>', parse_mode='html')

# func "help"
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, '<b><u>Выберите команду</u></b>', parse_mode='html', reply_markup=keyboard_client)
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting work schedule
async def get_work_schedule(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Режим работы: <u>с 7:00 до 18:00</u></b>', parse_mode='html', reply_markup=ReplyKeyboardRemove())
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting addres
async def get_address(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Адрес: <u>ул. Авилова</u></b>', parse_mode='html', reply_markup=ReplyKeyboardRemove())
    if(message.from_user.id != message.chat.id):
        await message.delete()

# func getting menu
async def get_menu(message: types.Message):
    await sqlite_db.sql_read(message)
    if(message.from_user.id != message.chat.id):
        await message.delete()

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(get_work_schedule, Text(equals='Режим работы', ignore_case=True))
    dp.register_message_handler(get_address, Text(equals='Адрес', ignore_case=True))
    dp.register_message_handler(get_menu, Text(equals='Меню', ignore_case=True))
