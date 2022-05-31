from email import message
from typing import Text
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client, keyboard_client_catalog
from keyboards import menu_start_state_init, menu_state_with_back, menu_start_state_with_description
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# basket shop
class basket:
    def __init__(self):
        # "name" : count
        self.content = {"chemical" : {}, "devices" : {}, "fertilizers" : {}, "seeds" : {}}

    def add(self, name_database, name_item):
        if self.content[name_database].get(name_item) is None:
            self.content[name_database][name_item] = 1
        else:
            self.content[name_database][name_item] += 1

    def remove(self, name_database, name_item):
        if self.content[name_database].get(name_item) is None:
            self.content[name_database][name_item] = 0
        elif self.content[name_database][name_item] > 0:
            self.content[name_database][name_item] -= 1


id = 12
client = {}

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
    client[message.from_user.id] = basket()
    await bot.send_message(message.from_user.id, '<b><u>🛎ВЫБЕРИТЕ РАЗДЕЛ🛎</u></b>', parse_mode='html', reply_markup=keyboard_client_catalog)
    if(message.from_user.id != message.chat.id):
        await message.delete()

async def get_menu(callback: types.CallbackQuery):
    read = await sqlite_db.sql_read(callback.data.replace("Client catalog ", ""))
    for item in read:
        # Тут добавь кнопну "Добавить в корзину"
        await callback.message.answer_photo(item[0], f'Название: {item[1]}\nЦена: {item[3]}', reply_markup=await menu_start_state_init(callback, item))
    await callback.answer()

async def get_description(callback: types.CallbackQuery):
    await callback.message.edit_caption(f'Описание: {callback.data.replace("description ", "")}',
    reply_markup=await menu_state_with_back(callback))

async def get_reverse(callback: types.CallbackQuery):
    await callback.message.edit_caption(f'{callback.data.replace("reverse ", "")}', parse_mode='html',
    reply_markup=await menu_start_state_with_description(callback))

async def add_basket(callback: types.CallbackQuery):
    split_data = callback.data.split()
    client[callback.from_user.id].add(split_data[3], split_data[4])
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Удалить из корзины", callback_data=f'remove from basket {split_data[3]} {split_data[4]}')))

async def remove_basket(callback: types.CallbackQuery):
    split_data = callback.data.split()
    client[callback.from_user.id].remove(split_data[3], split_data[4])
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Удалить из корзины", callback_data='del from basket')))


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(get_contact, Text(equals='☎️ Контакты ☎️', ignore_case=True))
    dp.register_message_handler(get_inforamation, Text(equals='🔎 О компании 🔍', ignore_case=True))
    dp.register_message_handler(get_catalog, Text(equals='🗂 Каталог 🗂', ignore_case=True))
    dp.register_callback_query_handler(get_menu, lambda x: x.data and x.data.startswith('Client catalog '))
    dp.register_callback_query_handler(get_description, lambda x: x.data and x.data.startswith('description '))
    dp.register_callback_query_handler(get_reverse, lambda x: x.data and x.data.startswith('reverse '))
    dp.register_callback_query_handler(add_basket, lambda x: x.data and x.data.startswith('add in basket '))
