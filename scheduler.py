"""Module 3 - Spaced repetition (SM-2) and priority-queue daily planner."""
import heapq
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Tuple

from . import config
from .database import Database
from .models import Topic


def sm2_update(ease: float, interval: int, repetitions: int, quality: int) -> Tuple[float, int, int]:
    """Return (new_ease, new_interval_days, new_repetitions) using the SM-2 algorithm."""
    if quality < 3:  # failed recall -> restart the learning sequence
        repetitions, interval = 0, 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = max(1, round(interval * ease))
        repetitions += 1
    ease = ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    return max(config.MIN_EASE, round(ease, 3)), interval, repetitions


def estimate_minutes(difficulty: int) -> int:
    """Rough time budget for one review of a topic."""
    return 10 + 5 * difficulty


@dataclass
class PlanItem:
    topic: Topic
    minutes: int
    overdue_days: int


class ReviewScheduler:
    def __init__(self, db: Database):
        self.db = db

    def apply_review(self, topic_id: int, quality: int, today: Optional[date] = None) -> Topic:
        today = today or date.today()
        row = self.db.query("SELECT * FROM topics WHERE id=?", (topic_id,))[0]
        ease, interval, reps = sm2_update(row["ease_factor"], row["interval_days"], row["repetitions"], quality)
        nxt = (today + timedelta(days=interval)).isoformat()
        self.db.execute(
            "UPDATE topics SET ease_factor=?, interval_days=?, repetitions=?, next_review=? WHERE id=?",
            (ease, interval, reps, nxt, topic_id),
        )
        return Topic(**dict(self.db.query("SELECT * FROM topics WHERE id=?", (topic_id,))[0]))

    def due_topics(self, today: Optional[date] = None) -> List[Topic]:
        """Topics never studied or with next_review <= today, most urgent first (min-heap)."""
        today = today or date.today()
        heap = []
        for r in self.db.query("SELECT * FROM topics"):
            t = Topic(**dict(r))
            if t.next_review is None:
                overdue = 0  # brand new topics
            else:
                overdue = (today - date.fromisoformat(t.next_review)).days
                if overdue < 0:
                    continue
            # smaller key = higher priority: most overdue, then hardest, then id
            heapq.heappush(heap, (-overdue, -t.difficulty, t.id, t))
        return [heapq.heappop(heap)[3] for _ in range(len(heap))]

    def daily_plan(self, available_minutes: int, today: Optional[date] = None) -> List[PlanItem]:
        """Greedily fill the time budget with the most urgent due topics."""
        today = today or date.today()
        plan, remaining = [], available_minutes
        for t in self.due_topics(today):
            need = estimate_minutes(t.difficulty)
            if need <= remaining:
                overdue = 0 if t.next_review is None else (today - date.fromisoformat(t.next_review)).days
                plan.append(PlanItem(t, need, overdue))
                remaining -= need
        return plan
