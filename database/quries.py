class Queries:
    CREATE_SURVEY_RESULTS_TABLE = """
        CREATE TABLE IF NOT EXISTS survey_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT ,
            visit_date TEXT ,
            food_rating INTEGER ,
            cleanliness_rating INTEGER ,
            additional_comments TEXT
        )
    """
