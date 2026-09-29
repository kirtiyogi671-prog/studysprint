"""SQLite persistence layer (single connection, parameterised queries only)."""
import sqlite3
from pathlib import Path

from .logger import get_logger

log = get_logger("studysprint.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    ease_factor REAL NOT NULL DEFAULT 2.5,
    interval_days INTEGER NOT NULL DEFAULT 0,
    repetitions INTEGER NOT NULL DEFAULT 0,
    next_review TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (subject_id, title)
);
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    minutes INTEGER NOT NULL CHECK (minutes > 0),
    quality INTEGER NOT NULL CHECK (quality BETWEEN 0 AND 5),
    notes TEXT NOT NULL DEFAULT '',
    studied_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_topics_next_review ON topics(next_review);
CREATE INDEX IF NOT EXISTS idx_sessions_topic ON sessions(topic_id);
"""


class Database:
    def __init__(self, path: str = ":memory:"):
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)
        log.info("Database ready at %s", path)

    def execute(self, sql: str, params: tuple = ()):
        try:
            with self.conn:  # auto commit / rollback
                return self.conn.execute(sql, params)
        except sqlite3.Error:
            log.exception("SQL failure: %s", sql)
            raise

    def query(self, sql: str, params: tuple = ()):
        return self.conn.execute(sql, params).fetchall()

    def close(self):
        self.conn.close()
