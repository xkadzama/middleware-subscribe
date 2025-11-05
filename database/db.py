import sqlite3


conn = sqlite3.connect('ruoms.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    category TEXT,
    amount_people TEXT,
    price FLOAT,
    status INTEGER,
    photo_id TEXT
    )
''')


conn.commit()
conn.close()
