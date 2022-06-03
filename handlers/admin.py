from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_admin, keyboard_admin_database, keyboard_admin_cancel_machine, keyboard_admin_delete_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
import json

with open('data_base/admin_key.json') as f:
    admins_id_array = set(json.load(f))
name_db = ''

async def moderator(message: types.Message):
    global admins_id_array
    admins_id_array.add(message.from_user.id)
    await bot.send_message(message.from_user.id, '<b><u>Теперь вы можете модерировать бота!</u></b>', parse_mode='html', reply_markup=keyboard_admin)
    await message.delete()

async def help_admin(message: types.Message):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    if(message.chat.id != message.from_user.id):
        await message.delete()
    await bot.send_message(message.from_user.id, '<b>Введите команду . . .</b>', parse_mode='html', reply_markup=keyboard_admin)

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

async def choice_db(message: types.Message):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    await bot.send_message(message.from_user.id, '<b><u>Выберите базу для загрузки</u></b>', parse_mode='html', reply_markup=keyboard_admin_database)

# Start state machie
async def sm_start(callback: types.CallbackQuery):
    global name_db
    name_db = callback.data.replace("Admin show catalog ", "")
    await FSMAdmin.photo.set()
    await callback.message.answer('Загрузи фото', reply_markup=keyboard_admin_cancel_machine)
    await callback.answer()

# Handler of cancel
async def cancel_handler(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    current_state = await state.get_state()
    if(current_state is None):
        return
    await state.finish()
    await bot.send_message(message.from_user.id, '<b>Машина состояний остановлена</b>', parse_mode='html', reply_markup=keyboard_admin)

# Get the 1st answer (Photo)
async def load_photo(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название")

# Get the 2nd answer (name)
async def load_name(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")

# Get the 3rd answer (description)
async def load_description(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Теперь укажи цену")

# Get the 4th answer (description) and clear state machine
async def load_price(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    global name_db
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sqlite_db.sql_add_command(state, name_db)
    await state.finish()
    await bot.send_message(message.from_user.id, '<b><u>Новый элемент успешно добавлен!</u></b>', parse_mode='html', reply_markup=keyboard_admin)

async def show_list(message: types.Message):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    await bot.send_message(message.from_user.id, '<b><u>Выберите базу для показа</u></b>', parse_mode='html', reply_markup=keyboard_admin_delete_db)

# func delete item menu for admin
async def delete_item(callback: types.CallbackQuery):
    global name_db
    name_db = callback.data.replace("Admin catalog del from ", "")
    read = await sqlite_db.sql_read(name_db)
    for item in read:
        await callback.message.answer_photo(item[0], f'Название: {item[1]}\nОписание: {item[2]}\n\
Цена: {item[3]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Удалить', callback_data=f'del {item[1]}')))
    await callback.answer()

async def del_callback_run(callback: types.CallbackQuery):
    global name_db
    await sqlite_db.sql_delete(callback.data.replace("del ", ""), name_db)
    await callback.answer(text=f'{callback.data.replace("del ", "")} Удален', show_alert=True)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(moderator, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(help_admin, commands=['help_admin'])
    dp.register_message_handler(choice_db, Text(equals='Загрузить', ignore_case=True), state=None)
    dp.register_callback_query_handler(sm_start, lambda x: x.data and x.data.startswith('Admin show catalog'), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Остановить загрузку', ignore_case=True), state=FSMAdmin)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(show_list, Text(equals='Показать весь список', ignore_case=True))
    dp.register_callback_query_handler(delete_item, lambda x: x.data and x.data.startswith('Admin catalog del from'))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
