from app.database.database import initialize_database


def create_tables() -> None:
    initialize_database()
