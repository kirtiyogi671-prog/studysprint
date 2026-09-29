"""Module 1 - Subject & topic management (CRUD)."""
import sqlite3
from typing import List, Optional

from .database import Database
from .logger import get_logger
from .models import Subject, Topic
from .validators import ValidationError, validate_difficulty, validate_name

log = get_logger("studysprint.subjects")


class SubjectManager:
    def __init__(self, db: Database):
        self.db = db

    # ---- subjects ----
    def add_subject(self, name: str) -> Subject:
        name = validate_name(name, "Subject name")
        try:
            cur = self.db.execute("INSERT INTO subjects(name) VALUES (?)", (name,))
        except sqlite3.IntegrityError:
            raise ValidationError(f"Subject '{name}' already exists.")
        log.info("Added subject %s", name)
        return self.get_subject(cur.lastrowid)

    def get_subject(self, subject_id: int) -> Subject:
        rows = self.db.query("SELECT * FROM subjects WHERE id=?", (subject_id,))
        if not rows:
            raise ValidationError(f"Subject #{subject_id} not found.")
        return Subject(**dict(rows[0]))

    def list_subjects(self) -> List[Subject]:
        return [Subject(**dict(r)) for r in self.db.query("SELECT * FROM subjects ORDER BY name")]

    def rename_subject(self, subject_id: int, new_name: str) -> Subject:
        self.get_subject(subject_id)
        new_name = validate_name(new_name, "Subject name")
        try:
            self.db.execute("UPDATE subjects SET name=? WHERE id=?", (new_name, subject_id))
        except sqlite3.IntegrityError:
            raise ValidationError(f"Subject '{new_name}' already exists.")
        return self.get_subject(subject_id)

    def delete_subject(self, subject_id: int) -> None:
        self.get_subject(subject_id)
        self.db.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
        log.info("Deleted subject #%s", subject_id)

    # ---- topics ----
    def add_topic(self, subject_id: int, title: str, difficulty: int = 3) -> Topic:
        self.get_subject(subject_id)
        title = validate_name(title, "Topic title")
        difficulty = validate_difficulty(difficulty)
        try:
            cur = self.db.execute(
                "INSERT INTO topics(subject_id,title,difficulty) VALUES (?,?,?)",
                (subject_id, title, difficulty),
            )
        except sqlite3.IntegrityError:
            raise ValidationError(f"Topic '{title}' already exists in this subject.")
        log.info("Added topic %s (subject %s)", title, subject_id)
        return self.get_topic(cur.lastrowid)

    def get_topic(self, topic_id: int) -> Topic:
        rows = self.db.query("SELECT * FROM topics WHERE id=?", (topic_id,))
        if not rows:
            raise ValidationError(f"Topic #{topic_id} not found.")
        return Topic(**dict(rows[0]))

    def list_topics(self, subject_id: Optional[int] = None) -> List[Topic]:
        if subject_id is None:
            rows = self.db.query("SELECT * FROM topics ORDER BY subject_id, title")
        else:
            rows = self.db.query("SELECT * FROM topics WHERE subject_id=? ORDER BY title", (subject_id,))
        return [Topic(**dict(r)) for r in rows]

    def update_difficulty(self, topic_id: int, difficulty: int) -> Topic:
        self.get_topic(topic_id)
        self.db.execute("UPDATE topics SET difficulty=? WHERE id=?", (validate_difficulty(difficulty), topic_id))
        return self.get_topic(topic_id)

    def delete_topic(self, topic_id: int) -> None:
        self.get_topic(topic_id)
        self.db.execute("DELETE FROM topics WHERE id=?", (topic_id,))
