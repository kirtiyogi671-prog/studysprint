"""Command-line interface tying the modules together."""
import argparse
import sys

from . import config
from .analytics import Analytics
from .database import Database
from .scheduler import ReviewScheduler
from .session_tracker import SessionTracker
from .subject_manager import SubjectManager
from .validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="studysprint", description="Study tracker with spaced repetition.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-subjects", help="List subjects")
    s = sub.add_parser("add-subject", help="Add a subject"); s.add_argument("name")
    s = sub.add_parser("delete-subject", help="Delete a subject"); s.add_argument("subject_id", type=int)
    s = sub.add_parser("add-topic", help="Add a topic")
    s.add_argument("subject_id", type=int); s.add_argument("title"); s.add_argument("-d", "--difficulty", type=int, default=3)
    s = sub.add_parser("list-topics", help="List topics"); s.add_argument("-s", "--subject", type=int)
    s = sub.add_parser("delete-topic", help="Delete a topic"); s.add_argument("topic_id", type=int)
    s = sub.add_parser("log", help="Log a study session")
    s.add_argument("topic_id", type=int); s.add_argument("minutes", type=int)
    s.add_argument("quality", type=int, help="Recall quality 0-5"); s.add_argument("-n", "--notes", default="")
    sub.add_parser("due", help="Topics due for review")
    s = sub.add_parser("plan", help="Build today's plan"); s.add_argument("minutes", type=int)
    sub.add_parser("report", help="Analytics report")
    s = sub.add_parser("export", help="Export sessions to CSV"); s.add_argument("path")
    return p


def run(args, db: Database) -> int:
    subjects, sched = SubjectManager(db), ReviewScheduler(db)
    tracker, stats = SessionTracker(db, sched), Analytics(db)
    c = args.cmd
    if c == "add-subject":
        x = subjects.add_subject(args.name); print(f"Added subject #{x.id}: {x.name}")
    elif c == "list-subjects":
        for x in subjects.list_subjects(): print(f"#{x.id:<3} {x.name}")
    elif c == "delete-subject":
        subjects.delete_subject(args.subject_id); print("Deleted.")
    elif c == "add-topic":
        t = subjects.add_topic(args.subject_id, args.title, args.difficulty)
        print(f"Added topic #{t.id}: {t.title} (difficulty {t.difficulty})")
    elif c == "list-topics":
        for t in subjects.list_topics(args.subject):
            print(f"#{t.id:<3} {t.title:<30} diff={t.difficulty} next={t.next_review or 'new'}")
    elif c == "delete-topic":
        subjects.delete_topic(args.topic_id); print("Deleted.")
    elif c == "log":
        sess = tracker.log_session(args.topic_id, args.minutes, args.quality, args.notes)
        t = subjects.get_topic(args.topic_id)
        print(f"Logged {sess.minutes} min. Next review: {t.next_review} (interval {t.interval_days}d, ease {t.ease_factor})")
    elif c == "due":
        due = sched.due_topics()
        print("Nothing due - great job!" if not due else "\n".join(f"#{t.id:<3} {t.title} (diff {t.difficulty})" for t in due))
    elif c == "plan":
        if args.minutes < 1: raise ValidationError("Minutes must be positive.")
        items = sched.daily_plan(args.minutes)
        for i in items: print(f"{i.minutes:>3} min  #{i.topic.id} {i.topic.title} (overdue {i.overdue_days}d)")
        print(f"Planned {sum(i.minutes for i in items)}/{args.minutes} min.")
    elif c == "report":
        print(stats.summary_text())
    elif c == "export":
        print(f"Exported {stats.export_csv(args.path)} sessions to {args.path}")
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    db = Database(config.DB_PATH)
    try:
        return run(args, db)
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr); return 1
    finally:
        db.close()
