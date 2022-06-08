import psycopg2 as ps
import os

# database for catalog
def sql_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()

def sql_finish():
    global base, cur
    base.close()
    cur.close()

async def sql_add_command(state, name_database):
    async with state.proxy() as data:
        if(name_database=='chemical'):
            cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        elif(name_database=='devices'):
            cur.execute('INSERT INTO devices VALUES (?, ?, ?, ?)', tuple(data.values()))
        elif(name_database=='fertilizers'):
            cur.execute('INSERT INTO fertilizers VALUES (?, ?, ?, ?)', tuple(data.values()))
        elif(name_database=='seeds'):
            cur.execute('INSERT INTO seeds VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(name_database):
    if(name_database=='chemical'):
        return cur.execute('SELECT * FROM chemical').fetchall()
    elif(name_database=='devices'):
        return cur.execute('SELECT * FROM devices').fetchall()
    elif(name_database=='fertilizers'):
        return cur.execute('SELECT * FROM fertilizers').fetchall()
    elif(name_database=='seeds'):
        return cur.execute('SELECT * FROM seeds').fetchall()

async def sql_get_description(name, name_database):
    if(name_database=='chemical'):
        return cur.execute('SELECT description FROM chemical WHERE name == ?', (name,)).fetchone()
    elif(name_database=='devices'):
        return cur.execute('SELECT description FROM devices WHERE name == ?', (name,)).fetchone()
    elif(name_database=='fertilizers'):
        return cur.execute('SELECT description FROM fertilizers WHERE name == ?', (name,)).fetchone()
    elif(name_database=='seeds'):
        return cur.execute('SELECT description FROM seeds WHERE name == ?', (name,)).fetchone()

async def sql_get_price(name, name_database):
    if(name_database=='chemical'):
        return cur.execute('SELECT price FROM chemical WHERE name == ?', (name,)).fetchone()
    elif(name_database=='devices'):
        return cur.execute('SELECT price FROM devices WHERE name == ?', (name,)).fetchone()
    elif(name_database=='fertilizers'):
        return cur.execute('SELECT price FROM fertilizers WHERE name == ?', (name,)).fetchone()
    elif(name_database=='seeds'):
        return cur.execute('SELECT price FROM seeds WHERE name == ?', (name,)).fetchone()

async def sql_delete(name, name_database):
    if(name_database=='chemical'):
        cur.execute('DELETE FROM chemical WHERE name == ?', (name,))
    elif(name_database=='devices'):
        cur.execute('DELETE FROM devices WHERE name == ?', (name,))
    elif(name_database=='fertilizers'):
        cur.execute('DELETE FROM fertilizers WHERE name == ?', (name,))
    elif(name_database=='seeds'):
        cur.execute('DELETE FROM seeds WHERE name == ?', (name,))
    base.commit()
