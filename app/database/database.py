import sqlite3

from app.config import DATABASE_PATH



def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection



def initialize_database():

    with get_connection() as connection:

        cursor = connection.cursor()


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),

                group_chat_id INTEGER,

                language TEXT DEFAULT 'uk',
                timezone TEXT DEFAULT 'Europe/Kyiv',

                prime_time TEXT,
                epics_schedule TEXT,
                announcement TEXT,

                reminders_enabled INTEGER DEFAULT 1,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)



        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prime_schedule (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                day_of_week INTEGER NOT NULL,

                start_time TEXT NOT NULL,

                end_time TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)



        cursor.execute("""
            INSERT INTO settings (
                id,
                language,
                timezone,
                reminders_enabled
            )
            VALUES (
                1,
                'uk',
                'Europe/Kyiv',
                1
            )
            ON CONFLICT(id) DO NOTHING
        """)


        connection.commit()