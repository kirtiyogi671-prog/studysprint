"""Fill a demo database with sample data so every feature can be tried immediately.

Usage:  STUDYSPRINT_DB=demo.db python scripts/seed_demo.py
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from studysprint import config
from studysprint.database import Database
from studysprint.scheduler import ReviewScheduler
from studysprint.session_tracker import SessionTracker
from studysprint.subject_manager import SubjectManager

db = Database(config.DB_PATH)
sm, tracker = SubjectManager(db), SessionTracker(db, ReviewScheduler(db))
if sm.list_subjects():
    sys.exit("Database already has data - use an empty database file.")

py, ds = sm.add_subject("Python"), sm.add_subject("Data Structures")
topics = [sm.add_topic(py.id, "Decorators", 4), sm.add_topic(py.id, "File Handling", 2),
          sm.add_topic(ds.id, "Binary Heaps", 5), sm.add_topic(ds.id, "Linked Lists", 3)]
now = datetime.now()
for days_ago, (t, mins, q) in enumerate([(topics[0], 45, 4), (topics[2], 60, 2), (topics[1], 30, 5), (topics[3], 40, 3)]):
    tracker.log_session(t.id, mins, q, "seed data", now - timedelta(days=3 - days_ago))
print("Demo data created in", config.DB_PATH)
