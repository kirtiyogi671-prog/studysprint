"""Module 2 - Study session logging (feeds the scheduler)."""
from datetime import datetime
from typing import List, Optional

from .database import Database
from .logger import get_logger
from .models import StudySession
from .scheduler import ReviewScheduler
from .validators import ValidationError, validate_minutes, validate_quality

log = get_logger("studysprint.sessions")


class SessionTracker:
    def __init__(self, db: Database, scheduler: ReviewScheduler):
        self.db = db
        self.scheduler = scheduler

    def log_session(self, topic_id: int, minutes: int, quality: int, notes: str = "",
                    when: Optional[datetime] = None) -> StudySession:
        if not self.db.query("SELECT 1 FROM topics WHERE id=?", (topic_id,)):
            raise ValidationError(f"Topic #{topic_id} not found.")
        minutes, quality = validate_minutes(minutes), validate_quality(quality)
        when = when or datetime.now()
        cur = self.db.execute(
            "INSERT INTO sessions(topic_id,minutes,quality,notes,studied_at) VALUES (?,?,?,?,?)",
            (topic_id, minutes, quality, (notes or "").strip()[:500], when.isoformat(timespec="seconds")),
        )
        self.scheduler.apply_review(topic_id, quality, when.date())
        log.info("Logged %s min on topic %s (quality %s)", minutes, topic_id, quality)
        return StudySession(**dict(self.db.query("SELECT * FROM sessions WHERE id=?", (cur.lastrowid,))[0]))

    def list_sessions(self, topic_id: Optional[int] = None, limit: int = 20) -> List[StudySession]:
        if topic_id is None:
            rows = self.db.query("SELECT * FROM sessions ORDER BY studied_at DESC LIMIT ?", (limit,))
        else:
            rows = self.db.query("SELECT * FROM sessions WHERE topic_id=? ORDER BY studied_at DESC LIMIT ?",
                                 (topic_id, limit))
        return [StudySession(**dict(r)) for r in rows]
