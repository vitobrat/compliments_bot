import aiosqlite

DATABASE = "bot.db"


async def create_table():
    async with aiosqlite.connect(DATABASE) as db:
        # Создание курсора
        cursor = await db.cursor()

        # Выполнение SQL-запроса с помощью курсора
        await cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        user_name TEXT,
        is_admin INTEGER
        )
        ''')

        # Коммит изменений
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''SELECT * FROM users WHERE user_id = ? 
        ''', (user_id,))
        row = await cursor.fetchone()
        return row


async def get_all_users():
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''SELECT * FROM users 
        ''')
        rows = await cursor.fetchall()
        return rows


async def add_user(user_id, user_fullname, user_username):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        check_user = await get_user(user_id)
        print(check_user)
        if check_user is None:
            await cursor.execute('''INSERT INTO users (user_id, full_name, user_name, is_admin) VALUES (?, ?, ?, ?)
            ''', (user_id, user_fullname, user_username, 0))
            await db.commit()


async def count_users():
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.cursor()
        await cursor.execute('''SELECT COUNT(*) FROM users 
        ''')
        count = await cursor.fetchone()
        return count[0]


