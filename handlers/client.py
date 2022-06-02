from typing import Text
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client, keyboard_client_catalog
from keyboards import menu_start_state_init, menu_state_with_back, menu_start_state_with_description
from keyboards import change_basket_state, confirmation_state, cancel_state, confirm_state
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

# basket shop
class basket:
    def __init__(self):
        # "name_catalog": {"name" : count}
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
        res = await callback.message.answer_photo(item[0], f'Название: {item[1]}\nЦена: {item[3]}')
        await res.edit_reply_markup(reply_markup=await menu_start_state_init(callback, item, res.message_id))
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
    await callback.message.edit_reply_markup(reply_markup=await change_basket_state(callback, client[callback.from_user.id].content[split_data[3]][split_data[4]]))
    await callback.answer()


async def remove_basket(callback: types.CallbackQuery):
    split_data = callback.data.split()
    if client[callback.from_user.id].content[split_data[3]][split_data[4]] == 0:
        await callback.answer()
        return
    client[callback.from_user.id].remove(split_data[3], split_data[4])
    await callback.message.edit_reply_markup(reply_markup=await change_basket_state(callback, client[callback.from_user.id].content[split_data[3]][split_data[4]]))
    await callback.answer()

async def send_basket(callback: types.CallbackQuery):
    split_data = callback.data.split()
    if client[callback.from_user.id].content[split_data[2]][split_data[3]] == 0:
        await callback.answer()
        return
    await callback.message.edit_reply_markup(reply_markup=await confirmation_state(callback))
    await callback.answer()

async def confirm_order(callback: types.CallbackQuery):
    split_data = callback.data.split()
    await bot.send_message(951719191, f"<b>От <u>{callback.from_user.first_name} {callback.from_user.username}</u> поступил заказ:</b>\n\
    Из раздела <u>{split_data[1]}</u> продукт <u>{split_data[2]}</u> в кол-ве: <i><b>{client[callback.from_user.id].content[split_data[1]][split_data[2]]}</b></i>",
        parse_mode='html')
    client[callback.from_user.id].content[split_data[1]][split_data[2]] = 1
    await callback.message.edit_reply_markup(reply_markup=await confirm_state(callback))
    await callback.answer()

async def cancel_order(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await cancel_state(callback))
    await callback.answer()

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(get_contact, Text(equals='☎️ Контакты ☎️', ignore_case=True))
    dp.register_message_handler(get_inforamation, Text(equals='🔎 О компании 🔍', ignore_case=True))
    dp.register_message_handler(get_catalog, Text(equals='🗂 Каталог 🗂', ignore_case=True))

    dp.register_callback_query_handler(get_menu, lambda x: x.data and x.data.startswith('Client catalog '))
    dp.register_callback_query_handler(get_description, lambda x: x.data and x.data.startswith('description '))
    dp.register_callback_query_handler(get_reverse, lambda x: x.data and x.data.startswith('reverse '))

    dp.register_callback_query_handler(add_basket, lambda x: x.data and x.data.startswith('add in basket '))
    dp.register_callback_query_handler(remove_basket, lambda x: x.data and x.data.startswith('remove from basket '))
    dp.register_callback_query_handler(send_basket, lambda x: x.data and x.data.startswith('send basket '))

    dp.register_callback_query_handler(confirm_order, lambda x: x.data and x.data.startswith('confirm '))
    dp.register_callback_query_handler(cancel_order, lambda x: x.data and x.data == 'cancel')
