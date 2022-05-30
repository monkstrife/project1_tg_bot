import sqlite3 as sq

base = {}

# database for catalog
def sql_start(text):
    base[text] = sq.connect(f'{text}.db')
    if base[text]:
        print('Data base connected OK!')
    base[text].execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base[text].commit()

async def sql_add_command(state, text):
    async with state.proxy() as data:
        cur = base[text].cursor()
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base[text].commit()

async def sql_read(text):
    cur = base[text].cursor()
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete(name, text):
    cur = base[text].cursor()
    cur.execute('DELETE FROM menu WHERE name == ?', (name,))
    base[text].commit()
