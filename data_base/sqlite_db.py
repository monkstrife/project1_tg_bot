import sqlite3 as sq
from create_bot import bot
from aiogram.types import ReplyKeyboardRemove

def sql_start():
    global base, cur
    base = sq.connect('products.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for element_db in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, element_db[0], f'Название: {element_db[1]}\nОписание: {element_db[2]}\n\
Цена: {element_db[3]}', parse_mode='html', reply_markup=ReplyKeyboardRemove())
