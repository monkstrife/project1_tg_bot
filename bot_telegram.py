from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db

# on startup func
async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_start()

# on shutdown func
async def on_shutdown(_):
    print("Бот отключен")
    sqlite_db.sql_finish()

# Client part
client.register_handler_client(dp)

# Admin part
admin.register_handler_admin(dp)

# Other part
other.register_handler_other(dp)

executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
