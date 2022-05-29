from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_admin
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

admins_id_array = set()

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

# Start state machie
async def sm_start(message: types.Message):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")

# Handler of cancel
async def cancel_handler(message: types.Message, state=FSMContext):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    current_state = await state.get_state()
    if(current_state is None):
        return
    await state.finish()
    await bot.send_message(message.from_user.id, '<b>Машина состояний остановлена</b>', parse_mode='html', reply_markup=ReplyKeyboardRemove())

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
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sqlite_db.sql_add_command(state)
    await state.finish()

# func delete item menu for admin
async def delete_item(message: types.Message):
    if admins_id_array.intersection(set([message.from_user.id])) == set():
        return
    read = await sqlite_db.sql_read()
    for item in read:
        await bot.send_photo(message.from_user.id, item[0], f'Название: {item[1]}\nОписание: {item[2]}\n\
Цена: {item[3]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Удалить', callback_data=f'del {item[1]}')))

async def del_callback_run(callback: types.CallbackQuery):
    await sqlite_db.sql_delete(callback.data.replace('del ', ''))
    await callback.answer(text=f'{callback.data.replace("del ", "")} Удален', show_alert=True)

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(moderator, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(help_admin, commands=['help_admin'])
    dp.register_message_handler(sm_start, Text(equals='Загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Остановить', ignore_case=True), state=FSMAdmin)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item, Text(equals='Показать весь список', ignore_case=True))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
