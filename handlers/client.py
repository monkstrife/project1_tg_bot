import telebot
from create_bot import bot
from keyboards import keyboard_client
from telebot.types import ReplyKeyboardRemove

# func start working
def start(message):
    bot.send_message(message.from_user.id, f'<b>Здравствуйте</b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, f'<b><u>{message.from_user.first_name}</u>, напишите боту в ЛС.\n@AgroSegmentBot</b>', parse_mode='html')

# func "help"
def help(message):
    if(message.from_user.id == message.chat.id):
        bot.send_message(message.from_user.id, '<b><u>Выберите команду</u></b>', parse_mode='html', reply_markup=keyboard_client)

# func getting work schedule
def get_work_schedule(message):
    if(message.text == 'Режим работы'):
        bot.send_message(message.from_user.id, '<b>Режим работы: <u>с 7:00 до 18:00</u></b>', parse_mode='html', reply_markup=ReplyKeyboardRemove())

# func getting addres
def get_address(message):
    if(message.text == 'Адрес'):
        bot.send_message(message.from_user.id, '<b>Адрес: <u>ул. Авилова</u></b>', parse_mode='html')

def launch_func(message):
    if(message.from_user.id == message.chat.id):
        get_work_schedule(message)
        get_address(message)

def register_handler_client():
    bot.register_message_handler(start, commands=['start'])
    bot.register_message_handler(help, commands=['help'])
    bot.register_message_handler(launch_func, content_types=['text'])
