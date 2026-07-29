from app.database.database import get_connection


def create_tables() -> None:
    """
    Создает все таблицы базы данных.
    """

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),

                group_chat_id INTEGER,
                language TEXT DEFAULT 'uk',
                timezone TEXT DEFAULT 'Europe/Kyiv',

                prime_time TEXT,
                prime_schedule TEXT,
                epics_schedule TEXT,
                announcement TEXT,

                reminders_enabled INTEGER DEFAULT 1,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()