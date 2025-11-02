import sqlite3
import os
from core import settings

class ScoreDataBase:
    def __init__(self, db_path=settings.DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()


    def _create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                initials TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()


    def insert_score(self, initials, score):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO scores (initials, score) VALUES (?, ?)", (initials, score))
        self.conn.commit()

    def get_top_scores(self, limit=5):
        cur = self.conn.cursor()
        cur.execute("SELECT initials, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return cur.fetchall()

    def is_top_score(self, score, limit=5):
        top_scores = self.get_top_scores(limit)
        if len(top_scores) < limit:
            return True
        return any(score > s[1] for s in top_scores)