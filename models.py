"""Plain data classes representing database rows."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Subject:
    id: int
    name: str
    created_at: str


@dataclass
class Topic:
    id: int
    subject_id: int
    title: str
    difficulty: int
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review: Optional[str]
    created_at: str


@dataclass
class StudySession:
    id: int
    topic_id: int
    minutes: int
    quality: int
    notes: str
    studied_at: str
