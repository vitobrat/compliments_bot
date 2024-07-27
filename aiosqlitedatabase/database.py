import aiosqlite

DATABASE = "bot.db"


async def create_table():
    async with aiosqlite.connect(DATABASE) as db:
        # Создание курсора
        cursor = await db.cursor()

        # Выполнение SQL-запроса с помощью курсора
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        user_name TEXT,
        send_mode INTEGER
        )
        ''')

        # Коммит изменений
        await db.commit()


async def get_user(user_id) -> set | None:
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''
        SELECT * FROM users WHERE user_id = ? 
        ''', (user_id,))
        row = await cursor.fetchone()
        return row


async def get_all_users() -> list | None:
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''
        SELECT * FROM users 
        ''')
        rows = await cursor.fetchall()
        return rows


async def add_user(user_id, user_fullname, user_username):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        check_user = await get_user(user_id)
        print(check_user)
        if check_user is None:
            await cursor.execute('''
            INSERT INTO users (user_id, full_name, user_name, send_mode) VALUES (?, ?, ?, ?)
            ''', (user_id, user_fullname, user_username, 0))
            await db.commit()


async def count_users() -> int:
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''
        SELECT COUNT(*) FROM users 
        ''')
        count = await cursor.fetchone()
        return count[0]


async def get_all_users_id() -> list | None:
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''
        SELECT user_id FROM users 
        ''')
        rows = await cursor.fetchall()
        return rows


async def get_all_users_id_with_send_mode() -> list | None:
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''
        SELECT user_id 
        FROM users 
        WHERE send_mode = 1 
        ''')
        rows = await cursor.fetchall()
        return rows


async def switch_on_send_mode_by_id(ids: list):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        # Создание строковых плейсхолдеров для параметров
        placeholders = ','.join(['?'] * len(ids))
        # Выполнение запроса с использованием параметров
        query = f'''
        UPDATE users
        SET send_mode = 1
        WHERE user_id IN ({placeholders})
        '''
        await cursor.execute(query, ids)
        await db.commit()


async def switch_off_send_mode_by_id(ids: list):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        # Создание строковых плейсхолдеров для параметров
        placeholders = ','.join(['?'] * len(ids))
        # Выполнение запроса с использованием параметров
        query = f'''
        UPDATE users
        SET send_mode = 0
        WHERE user_id IN ({placeholders})
        '''
        await cursor.execute(query, ids)
        await db.commit()


