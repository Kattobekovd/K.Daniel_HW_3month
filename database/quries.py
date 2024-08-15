class Queries:
    CREATE_SURVEY_RESULTS_TABLE = """
        CREATE TABLE IF NOT EXISTS survey_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            food_rating INTEGER NOT NULL,
            cleanliness_rating INTEGER NOT NULL,
            additional_comments TEXT
        )
    """
