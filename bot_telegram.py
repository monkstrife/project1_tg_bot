from aiogram.utils import executor
from create_bot import dp
from handlers import client, other

# on startup fuc
async def on_startup(_):
    print("Бот вышел в онлайн")

# Client part
client.register_handler_client(dp)

# Admin part


# Other part
other.register_handler_other(dp)

executor.start_polling(dp, on_startup=on_startup)
