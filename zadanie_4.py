import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def open_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users( 
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                who TEXT,
                age INT
            );
        """)
        self.connection.commit()

    def add_user(self, first_name, last_name, who, age):
        self.cursor.execute("SELECT * FROM users WHERE first_name=? AND last_name=?", (first_name, last_name))
        existing_user = self.cursor.fetchone()

        if existing_user:
            print(f"Пользователь с именем {first_name} {last_name} уже существует в базе данных.")
        else:
            self.cursor.execute("""
                INSERT INTO users (first_name, last_name, who, age) 
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, who, age))
            self.connection.commit()
            print(f"Пользователь {first_name} {last_name} был успешно добавлен.")

    def get_user(self, first_name=None, last_name=None):
        if first_name:
            self.cursor.execute("SELECT * FROM users WHERE first_name=?", (first_name,))
        elif last_name:
            self.cursor.execute("SELECT * FROM users WHERE last_name=?", (last_name,))
        else:
            return None

        return self.cursor.fetchone()

    def delete_user(self, first_name=None, last_name=None):
        if first_name:
            self.cursor.execute("SELECT * FROM users WHERE first_name=?", (first_name,))
        elif last_name:
            self.cursor.execute("SELECT * FROM users WHERE last_name=?", (last_name,))
        else:
            print("Необходимо указать имя или фамилию пользователя для удаления.")
            return
        
        user = self.cursor.fetchone()

        if user:
            self.cursor.execute("DELETE FROM users WHERE id=?", (user[0],))
            self.connection.commit()
            print(f"Пользователь {user[1]} {user[2]} был успешно удален.")
        else:
            print(f"Пользователь не найден в базе данных.")

db_manager = DatabaseManager('users.db')

db_manager.open_connection()

db_manager.create_table()

db_manager.add_user('Artyk', 'Erkhan', 'Клиент', 14)
db_manager.add_user('Isajanov', 'Isa', 'Клиент', 20)
db_manager.add_user('Wohavich', 'Woha', 'Админ', 19)

user = db_manager.get_user(first_name='Wohavich')
print(user)

db_manager.delete_user(first_name='Artyk')

db_manager.delete_user(last_name='Isa')

db_manager.delete_user(first_name='Nonexistent')

db_manager.close_connection()
