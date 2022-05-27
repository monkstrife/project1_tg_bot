import telebot
from create_bot import bot
from handlers import client, other

# Client part
client.register_handler_client()

# Admin part


# Other part
other.register_handler_other()

bot.polling(non_stop=True)
