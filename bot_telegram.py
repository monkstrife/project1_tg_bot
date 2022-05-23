import telebot
import os

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(func= lambda mess: mess.text == 'привет')
def start(message):
    bot.send_message(message.from_user.id, f'<b>{message.text}</b>', parse_mode='html')

bot.polling(non_stop=True)
