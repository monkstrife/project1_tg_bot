import telebot
import os

#token = os.getenv('TOKEN')
bot = telebot.TeleBot('5318034841:AAE8LwugFT2Ne-cRpFH6QdJ0mD398M2WiYU')

################## Клиентская часть #####################

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.from_user.id, f'<b>Здравствуйте</b>', parse_mode='html')
    if(message.from_user.id != message.chat.id):
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, f'<b><u>{message.from_user.first_name}</u>, напишите боту в ЛС.\n@AgroSegmentBot</b>', parse_mode='html')

@bot.message_handler(commands=['режим_работы', 'work_schedule'])
def work_schedule(message):
    if(message.from_user.id == message.chat.id):
        bot.send_message(message.from_user.id, '<b>Режим работы: <u>с 7:00 до 18:00</u></b>', parse_mode='html')

@bot.message_handler(commands=['адрес', 'address'])
def work_schedule(message):
    if(message.from_user.id == message.chat.id):
        bot.send_message(message.from_user.id, '<b>Адрес: <u>ул. Авилова</u></b>', parse_mode='html')

################### Админская часть #####################



#################### Общая часть ########################

@bot.message_handler()
def start(message):
    pass

bot.polling(non_stop=True)
