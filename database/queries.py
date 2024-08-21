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

    CREATE_TABLE_CATEGORIES = '''
    CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    UNIQUE(name))'''

    CREATE_TABLE_DISHES = '''
    CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    price INTEGER,
    photo TEXT,
    category_id INTEGER,
    UNIQUE(title), 
    FOREIGN KEY(category_id) REFERENCES categories(id))'''

    INSERT_INTO_CAT = '''
    INSERT OR IGNORE INTO categories (name) VALUES ('drinks'),('first'),('second')'''

    INSERT_INTO_DISHES = '''
    INSERT OR IGNORE INTO dishes (title,price ,photo ,category_id) VALUES ('Босо Лагман',250,'images/Lagman.jpg',2),
    ('Борщ',200,'images/Borsh.jpg',3),
    ('Коктейл',100,'images/kok.jpg',1)'''
