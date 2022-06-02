from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db

# on startup fuc
async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_start('chemical')
    sqlite_db.sql_start('devices')
    sqlite_db.sql_start('fertilizers')
    sqlite_db.sql_start('seeds')

# Client part
client.register_handler_client(dp)

# Admin part
admin.register_handler_admin(dp)

# Other part
other.register_handler_other(dp)

executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
