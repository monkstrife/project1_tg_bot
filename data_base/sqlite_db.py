import sqlite3 as sq

base = {}

# database for catalog
def sql_start(name_database):
    base[name_database] = sq.connect(f'{name_database}.db')
    if base[name_database]:
        print('Data base connected OK!')
    base[name_database].execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base[name_database].commit()

async def sql_add_command(state, name_database):
    async with state.proxy() as data:
        cur = base[name_database].cursor()
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base[name_database].commit()

async def sql_read(name_database):
    cur = base[name_database].cursor()
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_get_description(name, name_database):
    cur = base[name_database].cursor()
    return cur.execute('SELECT description FROM menu WHERE name == ?', (name,)).fetchone()

async def sql_get_price(name, name_database):
    cur = base[name_database].cursor()
    return cur.execute('SELECT price FROM menu WHERE name == ?', (name,)).fetchone()

async def sql_delete(name, name_database):
    cur = base[name_database].cursor()
    cur.execute('DELETE FROM menu WHERE name == ?', (name,))
    base[name_database].commit()
