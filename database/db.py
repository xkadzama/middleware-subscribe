import sqlite3

class DataManager:
    def __init__(self, db_name='rooms.db'):
        self.db_name = db_name

    def db_connect(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor

    def init_database(self):
        conn, cursor = self.db_connect()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount_people INTEGER,
            price FLOAT,
            status INTEGER,
            photo_id TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_rooms(self, category: str, amount_people: str,
                  price: float, status: int, photo_id: str = None):
        conn, cursor = self.db_connect()
        try:
            cursor.execute('''
                        INSERT INTO rooms (category, amount_people, price, status, photo_id)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (category, amount_people, price, status, photo_id))
            conn.commit()
            return {'status': 200}
        except Exception as e:
            print(f'Ошибка БД: {e}')
        finally:
            print('conn.close()')
            conn.close()

    def get_available_rooms(self):
        conn, cursor = self.db_connect()

        cursor.execute('SELECT * FROM rooms WHERE status = 2')
        rooms = cursor.fetchall()
        conn.close()
        return rooms

class ReactionManager:
    def __init__(self, db_name='rooms.db'):
        self.db_name = db_name

    def db_connect(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor

    def init_database(self):
        conn, cursor = self.db_connect()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_reactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    room_id INTEGER NOT NULL,
                    reaction TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, room_id)
                )
            ''')
        conn.commit()
        conn.close()

    def add_reaction(self, user_id, room_id, reaction: str):
        conn, cursor = self.db_connect()
        cursor.execute('''
                    INSERT OR REPLACE INTO user_reactions 
                    (user_id, room_id, reaction) 
                    VALUES (?, ?, ?)
                ''', (user_id, room_id, reaction))

        conn.commit()
        conn.close()

    def get_user_reactions(self, user_id: int):
        conn, cursor = self.db_connect()
        cursor.execute('''
        SELECT * FROM rooms r
        JOIN user_reactions ur ON r.id = ur.room_id,
        WHERE ur.user_id = ?''')
        rooms = cursor.fetchall()
        conn.close()
        return rooms

db_manager = DataManager()
db_reactor = ReactionManager()