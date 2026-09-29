import os
import tempfile
import unittest
from datetime import date, datetime
from studysprint.analytics import Analytics
from studysprint.database import Database
from studysprint.scheduler import ReviewScheduler
from studysprint.session_tracker import SessionTracker
from studysprint.subject_manager import SubjectManager


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        sm = SubjectManager(self.db)
        py = sm.add_subject("Python"); ma = sm.add_subject("Maths")
        self.t1 = sm.add_topic(py.id, "Loops"); self.t2 = sm.add_topic(ma.id, "Calculus")
        self.tr = SessionTracker(self.db, ReviewScheduler(self.db))
        self.an = Analytics(self.db)
        self.tr.log_session(self.t1.id, 60, 5, when=datetime(2026, 3, 8, 9))
        self.tr.log_session(self.t1.id, 30, 4, when=datetime(2026, 3, 9, 9))
        self.tr.log_session(self.t2.id, 45, 2, when=datetime(2026, 3, 10, 9))

    def test_minutes_by_subject(self):
        self.assertEqual(self.an.minutes_by_subject(), {"Python": 90, "Maths": 45})

    def test_streak(self):
        self.assertEqual(self.an.current_streak(date(2026, 3, 10)), 3)
        self.assertEqual(self.an.current_streak(date(2026, 3, 11)), 3)  # yesterday counts
        self.assertEqual(self.an.current_streak(date(2026, 3, 13)), 0)

    def test_weakest_and_daily(self):
        self.assertEqual(self.an.weakest_topics(1)[0]["title"], "Calculus")
        d = self.an.daily_minutes(3, date(2026, 3, 10))
        self.assertEqual(list(d.values()), [60, 30, 45])

    def test_export_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "out.csv")
            self.assertEqual(self.an.export_csv(p), 3)
            self.assertEqual(len(open(p).read().strip().splitlines()), 4)
        self.assertIn("Total study time : 135 min", self.an.summary_text(date(2026, 3, 10)))

    def test_empty_db(self):
        an = Analytics(Database(":memory:"))
        self.assertEqual(an.current_streak(), 0)
        self.assertIn("Total study time : 0", an.summary_text())


if __name__ == "__main__":
    unittest.main()
