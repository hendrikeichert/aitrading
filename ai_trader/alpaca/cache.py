import os
import sqlite3

class DataCache:

    def __init__(self, filepath:str="data", filename:str="news_cache.db"):
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        self.db_file =  f'{filepath}/{filename}'
        self.init_db()

    def _create_news_table(self, cursor):
        # Create table for news
        cursor.execute('''CREATE TABLE IF NOT EXISTS news(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    content TEXT,
                    created_at TEXT,
                    headline TEXT,
                    source TEXT,
                    summary TEXT,
                    updated_at TEXT,
                    url TEXT,
                    -- For images, we'll store them as JSON since we have multiple entries with different sizes
                    images TEXT,
                    -- For symbols, we'll also store them as JSON due to the list nature
                    symbols TEXT
                )''')
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_headline ON news (headline)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON news (created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON news (source)")

    def _create_url_content_table(self, cursor):
                # Create table for articles
        cursor.execute('''CREATE TABLE IF NOT EXISTS url_content (
                    news_id INTEGER PRIMARY KEY,
                    url TEXT UNIQUE,
                    content TEXT)''')
        
    def init_db(self):
        # if os.path.exists(self.db_file): 
        #     print("Database already exists. Skipping creation.")
        #     return
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        self._create_news_table(cursor)
        self._create_url_content_table(cursor)
        conn.commit()
        conn.close()

    def save_news(self, news_list):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for news_item in news_list:
            cursor.execute('''INSERT INTO news (author, content, created_at, headline, source, summary, updated_at, url, images, symbols) 
                VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (news_item["author"], news_item["content"], news_item["created_at"], news_item["headline"], news_item["source"], news_item["summary"], news_item["updated_at"], news_item["url"], news_item["images"], news_item["symbols"]))
        conn.commit()
        conn.close()
    

        
