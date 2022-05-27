import telebot
from create_bot import bot

# func start working
def start(message):
    bot.send_message(message.from_user.id, f'<b>Здравствуйте</b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, f'<b><u>{message.from_user.first_name}</u>, напишите боту в ЛС.\n@AgroSegmentBot</b>', parse_mode='html')

# func getting work schedule
def get_work_schedule(message):
    if(message.from_user.id == message.chat.id):
        bot.send_message(message.from_user.id, '<b>Режим работы: <u>с 7:00 до 18:00</u></b>', parse_mode='html')

# func getting addres
def get_address(message):
    if(message.from_user.id == message.chat.id):
        bot.send_message(message.from_user.id, '<b>Адрес: <u>ул. Авилова</u></b>', parse_mode='html')

def register_handler_client():
    bot.register_message_handler(start, commands=['start', 'help'])
    bot.register_message_handler(get_work_schedule, commands=['режим_работы', 'work_schedule'])
    bot.register_message_handler(get_address, commands=['адрес', 'address'])
