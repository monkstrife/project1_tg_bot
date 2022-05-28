from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_admin
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

async def help_admin(message: types.Message):
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
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")

# Handler of cancel
async def cancel_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if(current_state is None):
        return
    await state.finish()
    await bot.send_message(message.from_user.id, '<b>Машина состояний остановлена</b>', parse_mode='html', reply_markup=ReplyKeyboardRemove())

# Get the 1st answer (Photo)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название")

# Get the 2nd answer (name)
async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")

# Get the 3rd answer (description)
async def load_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Теперь укажи цену")

# Get the 4th answer (description) and clear state machine
async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(help_admin, commands=['help_admin'])
    dp.register_message_handler(sm_start, Text(equals='Загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Остановить', ignore_case=True), state=FSMAdmin)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
