import sqlite3
from database.queries import Queries


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(Queries.CREATE_SURVEY_RESULTS_TABLE)
            conn.execute(Queries.CREATE_TABLE_DISHES)
            conn.execute(Queries.CREATE_TABLE_CATEGORIES)
            conn.execute(Queries.INSERT_INTO_CAT)
            conn.execute(Queries.INSERT_INTO_DISHES)
            conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
