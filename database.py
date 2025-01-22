import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS review")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS review (
                name TEXT,
                phone_number TEXT,
                rate INTEGER,
                extra_comments TEXT
            )
            """)
            conn.commit()

    def save_review(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO review (name, phone_number, rate, extra_comments)
                VALUES (?, ?, ?, ?)
                """,
                (data["name"], data["phone_number"], data["rate"], data["extra_comments"])
            )
            conn.commit()
