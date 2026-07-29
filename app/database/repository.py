from app.database import get_connection


class SettingsRepository:


    @staticmethod
    def get_settings():

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM settings
                WHERE id = 1
            """)

            return cursor.fetchone()



    @staticmethod
    def create_default_settings():

        with get_connection() as connection:
            cursor = connection.cursor()

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



    @staticmethod
    def update_group_chat(chat_id: int):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE settings
                SET group_chat_id = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                chat_id,
            ))

            connection.commit()



    # =========================
    # ПРАЙМ
    # =========================


    @staticmethod
    def update_prime_time(prime_time: str):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE settings
                SET prime_time = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                prime_time,
            ))

            connection.commit()



    @staticmethod
    def get_prime_schedule():

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT prime_time
                FROM settings
                WHERE id = 1
            """)

            result = cursor.fetchone()

            if result:
                return result["prime_time"]

            return None



    @staticmethod
    def clear_prime_schedule():

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM prime_schedule
            """)

            connection.commit()



    @staticmethod
    def add_prime_day(
        day: int,
        start_time: str,
        end_time: str
    ):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO prime_schedule (
                    day_of_week,
                    start_time,
                    end_time
                )
                VALUES (?, ?, ?)
            """, (
                day,
                start_time,
                end_time
            ))

            connection.commit()



    @staticmethod
    def get_today_prime(day: int):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM prime_schedule
                WHERE day_of_week = ?
            """, (
                day,
            ))

            return cursor.fetchone()



    # =========================
    # ЭПИКИ
    # =========================


    @staticmethod
    def update_epics_schedule(text: str):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE settings
                SET epics_schedule = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                text,
            ))

            connection.commit()



    @staticmethod
    def get_epics_schedule():

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT epics_schedule
                FROM settings
                WHERE id = 1
            """)

            result = cursor.fetchone()

            if result:
                return result["epics_schedule"]

            return None



    # =========================
    # ОГОЛОШЕННЯ
    # =========================


    @staticmethod
    def update_announcement(text: str):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE settings
                SET announcement = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                text,
            ))

            connection.commit()



    @staticmethod
    def get_announcement():

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT announcement
                FROM settings
                WHERE id = 1
            """)

            result = cursor.fetchone()

            if result:
                return result["announcement"]

            return None



    # =========================
    # НАПОМИНАНИЯ
    # =========================


    @staticmethod
    def set_reminders(enabled: bool):

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE settings
                SET reminders_enabled = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                1 if enabled else 0,
            ))

            connection.commit()