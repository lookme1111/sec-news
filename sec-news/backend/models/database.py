import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path='/app/data/news.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE,
                source TEXT,
                publish_date DATETIME,
                content TEXT,
                category TEXT,
                severity TEXT,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cve_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT UNIQUE,
                summary TEXT,
                published_date DATETIME,
                cvss_score REAL,
                severity TEXT,
                references TEXT,
                affected_products TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_date ON security_news(publish_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cve_date ON cve_data(published_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cve_score ON cve_data(cvss_score)')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn