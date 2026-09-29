"""Module 4 - Reporting & analytics (aggregations, streaks, CSV export)."""
import csv
from datetime import date, timedelta
from typing import Dict, List, Optional

from .database import Database


class Analytics:
    def __init__(self, db: Database):
        self.db = db

    def minutes_by_subject(self) -> Dict[str, int]:
        rows = self.db.query(
            """SELECT s.name, COALESCE(SUM(se.minutes),0) AS total FROM subjects s
               LEFT JOIN topics t ON t.subject_id=s.id LEFT JOIN sessions se ON se.topic_id=t.id
               GROUP BY s.id ORDER BY total DESC""")
        return {r["name"]: r["total"] for r in rows}

    def average_quality_by_subject(self) -> Dict[str, float]:
        rows = self.db.query(
            """SELECT s.name, AVG(se.quality) AS q FROM subjects s
               JOIN topics t ON t.subject_id=s.id JOIN sessions se ON se.topic_id=t.id GROUP BY s.id""")
        return {r["name"]: round(r["q"], 2) for r in rows}

    def weakest_topics(self, limit: int = 3) -> List[dict]:
        rows = self.db.query(
            """SELECT t.title, s.name AS subject, ROUND(AVG(se.quality),2) AS avg_q FROM topics t
               JOIN subjects s ON s.id=t.subject_id JOIN sessions se ON se.topic_id=t.id
               GROUP BY t.id ORDER BY avg_q ASC, t.title LIMIT ?""", (limit,))
        return [dict(r) for r in rows]

    def daily_minutes(self, days: int = 7, today: Optional[date] = None) -> Dict[str, int]:
        today = today or date.today()
        start = today - timedelta(days=days - 1)
        rows = self.db.query(
            "SELECT substr(studied_at,1,10) AS d, SUM(minutes) AS m FROM sessions WHERE d>=? GROUP BY d",
            (start.isoformat(),))
        got = {r["d"]: r["m"] for r in rows}
        return {(start + timedelta(days=i)).isoformat(): got.get((start + timedelta(days=i)).isoformat(), 0)
                for i in range(days)}

    def current_streak(self, today: Optional[date] = None) -> int:
        """Consecutive days (ending today or yesterday) with at least one session."""
        today = today or date.today()
        days = {r["d"] for r in self.db.query("SELECT DISTINCT substr(studied_at,1,10) AS d FROM sessions")}
        cursor = today if today.isoformat() in days else today - timedelta(days=1)
        streak = 0
        while cursor.isoformat() in days:
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def summary_text(self, today: Optional[date] = None) -> str:
        lines = ["=== StudySprint Report ==="]
        mins = self.minutes_by_subject()
        lines.append(f"Total study time : {sum(mins.values())} min")
        lines.append(f"Current streak   : {self.current_streak(today)} day(s)")
        lines.append("\nMinutes per subject:")
        for name, m in mins.items():
            lines.append(f"  {name:<20} {m:>5} min  {'#' * min(30, m // 10)}")
        lines.append("\nLast 7 days:")
        for d, m in self.daily_minutes(7, today).items():
            lines.append(f"  {d}  {m:>4} min")
        weak = self.weakest_topics()
        if weak:
            lines.append("\nTopics needing attention:")
            for w in weak:
                lines.append(f"  {w['subject']} / {w['title']} (avg recall {w['avg_q']}/5)")
        return "\n".join(lines)

    def export_csv(self, path: str) -> int:
        rows = self.db.query(
            """SELECT se.studied_at, s.name AS subject, t.title AS topic, se.minutes, se.quality, se.notes
               FROM sessions se JOIN topics t ON t.id=se.topic_id JOIN subjects s ON s.id=t.subject_id
               ORDER BY se.studied_at""")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["studied_at", "subject", "topic", "minutes", "quality", "notes"])
            for r in rows:
                w.writerow(list(r))
        return len(rows)
