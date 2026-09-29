import unittest
from datetime import date, timedelta
from studysprint.database import Database
from studysprint.scheduler import ReviewScheduler, sm2_update, estimate_minutes
from studysprint.subject_manager import SubjectManager

TODAY = date(2026, 3, 10)


class TestSM2(unittest.TestCase):
    def test_interval_progression(self):
        e, i, r = sm2_update(2.5, 0, 0, 5)
        self.assertEqual((i, r), (1, 1))
        e, i, r = sm2_update(e, i, r, 5)
        self.assertEqual((i, r), (6, 2))
        e, i, r = sm2_update(e, i, r, 5)
        self.assertEqual(i, 16)  # round(6 * 2.7)

    def test_failure_resets(self):
        e, i, r = sm2_update(2.5, 15, 4, 1)
        self.assertEqual((i, r), (1, 0))
        self.assertLess(e, 2.5)

    def test_ease_floor(self):
        e = 1.35
        for _ in range(5):
            e, _, _ = sm2_update(e, 1, 0, 0)
        self.assertGreaterEqual(e, 1.3)

    def test_estimate(self):
        self.assertEqual(estimate_minutes(1), 15)
        self.assertEqual(estimate_minutes(5), 35)


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.sm = SubjectManager(self.db)
        self.sch = ReviewScheduler(self.db)
        self.s = self.sm.add_subject("S")

    def test_new_topics_are_due(self):
        self.sm.add_topic(self.s.id, "A")
        self.assertEqual(len(self.sch.due_topics(TODAY)), 1)

    def test_apply_review_sets_next_date(self):
        t = self.sm.add_topic(self.s.id, "A")
        t2 = self.sch.apply_review(t.id, 5, TODAY)
        self.assertEqual(t2.next_review, (TODAY + timedelta(days=1)).isoformat())
        self.assertEqual(self.sch.due_topics(TODAY), [])
        self.assertEqual(len(self.sch.due_topics(TODAY + timedelta(days=1))), 1)

    def test_priority_order_most_overdue_first(self):
        a = self.sm.add_topic(self.s.id, "A", 2)
        b = self.sm.add_topic(self.s.id, "B", 2)
        self.db.execute("UPDATE topics SET next_review=? WHERE id=?", ("2026-03-01", a.id))
        self.db.execute("UPDATE topics SET next_review=? WHERE id=?", ("2026-03-08", b.id))
        self.assertEqual([t.title for t in self.sch.due_topics(TODAY)], ["A", "B"])

    def test_daily_plan_respects_budget(self):
        for n in "ABC":
            self.sm.add_topic(self.s.id, n, 3)  # 25 min each
        plan = self.sch.daily_plan(60, TODAY)
        self.assertEqual(len(plan), 2)
        self.assertLessEqual(sum(p.minutes for p in plan), 60)
        self.assertEqual(self.sch.daily_plan(5, TODAY), [])


if __name__ == "__main__":
    unittest.main()
