import sqlite3




class DataManager:
    def __init__(self, db_name='rooms'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('rooms.db')
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

    def add_rooms(self, category: str, amount_people: str, price: float, status: int, photo_id: str = None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
                    INSERT INTO rooms (category, amount_people, price, status, photo_id)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (category, amount_people, price, status, photo_id))

        conn.commit()

    def get_available_rooms(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE status = 2')
        rooms = cursor.fetchall()
        conn.close()
        return rooms


db_manager = DataManager()