import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS review(
                name TEXT,
                phone_number TEXT,
                rate INTEGER,
                extra_comments TEXT
            )
            """)
            conn.commit()

            conn.execute("""
                        CREATE TABLE IF NOT EXISTS menu(
                            dish_name TEXT,
                            description TEXT,
                            price INTEGER,
                            category TEXT, 
                            serving_size TEXT
                        )
                        """)

            conn.commit()

    def save_review(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO review (name, phone_number, rate, extra_comments)
                VALUES (?, ?, ?, ?)
                """,
                (data["name"], data["phone_number"], data["rate"], data["extra_comments"])
            )
            conn.commit()

    def save_menu_item(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO menu (dish_name, description, price, category, serving_size)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (data["dish_name"], data["description"], data["price"], data["category"], data["serving_size"]))
            conn.commit()


    def get_all_dishes(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM menu")
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]

    def get_all_reviews(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM review")
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]


