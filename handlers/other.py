from aiogram import types, Dispatcher
from create_bot import bot
import json, string

async def mat_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))):
        await bot.send_message(message.from_user.id, '<u><b>Маты запрещены!</b></u>', parse_mode='html')
        await message.delete()

def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(mat_filter)
