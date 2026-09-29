import unittest
from datetime import datetime
from studysprint.database import Database
from studysprint.scheduler import ReviewScheduler
from studysprint.session_tracker import SessionTracker
from studysprint.subject_manager import SubjectManager
from studysprint.validators import ValidationError


class TestSessionTracker(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        sm = SubjectManager(self.db)
        self.t = sm.add_topic(sm.add_subject("S").id, "T")
        self.tr = SessionTracker(self.db, ReviewScheduler(self.db))

    def test_log_updates_schedule(self):
        s = self.tr.log_session(self.t.id, 30, 4, "ok", datetime(2026, 3, 10, 9, 0))
        self.assertEqual(s.minutes, 30)
        row = self.db.query("SELECT next_review, repetitions FROM topics")[0]
        self.assertEqual(row["next_review"], "2026-03-11")
        self.assertEqual(row["repetitions"], 1)

    def test_validation(self):
        with self.assertRaises(ValidationError): self.tr.log_session(999, 10, 3)
        with self.assertRaises(ValidationError): self.tr.log_session(self.t.id, 0, 3)
        with self.assertRaises(ValidationError): self.tr.log_session(self.t.id, 10, 9)
        self.assertEqual(self.tr.list_sessions(), [])

    def test_list_sessions_order(self):
        self.tr.log_session(self.t.id, 10, 3, when=datetime(2026, 3, 1, 8))
        self.tr.log_session(self.t.id, 20, 3, when=datetime(2026, 3, 2, 8))
        self.assertEqual([s.minutes for s in self.tr.list_sessions()], [20, 10])


if __name__ == "__main__":
    unittest.main()
