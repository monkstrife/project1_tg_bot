import telebot
from create_bot import bot
import json, string

def mat_filter(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))):
        bot.send_message(message.from_user.id, '<u><b>Маты запрещены!</b></u>', parse_mode='html')
        bot.delete_message(message.chat.id, message.id)

def register_handler_other():
    bot.register_message_handler(mat_filter)
