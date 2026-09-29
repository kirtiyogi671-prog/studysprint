"""Generates StudySprint_Project_Report.pdf (reportlab)."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
                                ListFlowable, ListItem)
from PIL import Image as PILImage

IMG = "img/"
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, spaceBefore=6, spaceAfter=8, textColor=colors.HexColor("#1f3a93"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10.5, leading=15)
CAP = ParagraphStyle("CAP", parent=B, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
CODE = ParagraphStyle("CODE", parent=B, fontName="Courier", fontSize=8.5, leading=11, backColor=colors.HexColor("#f4f4f4"))
story = []


def p(t): story.append(Paragraph(t, B))
def h1(t): story.append(Paragraph(t, H1))
def h2(t): story.append(Paragraph(t, H2))
def bl(items): story.append(ListFlowable([ListItem(Paragraph(i, B)) for i in items], bulletType="bullet", leftIndent=16))


def img(name, caption, maxw=16.5 * cm, maxh=19 * cm):
    w, h = PILImage.open(IMG + name).size
    s = min(maxw / w, maxh / h)
    story.append(Image(IMG + name, w * s, h * s)); story.append(Paragraph(caption, CAP)); story.append(Spacer(1, 8))


def table(rows, widths, head=True):
    t = Table([[Paragraph(str(c), ParagraphStyle("t", parent=B, fontSize=9, leading=12)) for c in r] for r in rows], colWidths=widths)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7fb")))
    t.setStyle(TableStyle(st)); story.append(t); story.append(Spacer(1, 8))


# 1 Cover
story += [Spacer(1, 4 * cm), Paragraph("VITyarthi - Build Your Own Project", ParagraphStyle("c0", parent=B, alignment=TA_CENTER, fontSize=13)),
          Spacer(1, 1 * cm), Paragraph("StudySprint", ParagraphStyle("c1", parent=ss["Title"], fontSize=38, textColor=colors.HexColor("#1f3a93"))),
          Paragraph("Smart Study Tracker with Spaced-Repetition Scheduling", ParagraphStyle("c2", parent=B, alignment=TA_CENTER, fontSize=15)),
          Spacer(1, 2 * cm)]
table([["Course", "Python Programming"], ["Project type", "Individual - Build Your Own Project"], ["Student name", "Kirti Yogi"],
       ["Registration no.", "24MIM10188"], ["Faculty", "Ashok Patel"], ["Slot", "B21+B22+B23+E14+E21+E22"], ["Date", "September 2026"],
       ["GitHub repository", "https://github.com/kirtiyogi671/studysprint"]], [5 * cm, 10 * cm], head=False)
story.append(PageBreak())

# Contents
h1("Table of Contents")
for i, t in enumerate(["Introduction", "Problem Statement", "Functional Requirements", "Non-functional Requirements", "System Architecture",
                       "Design Diagrams", "Design Decisions & Rationale", "Implementation Details", "Screenshots / Results", "Testing Approach",
                       "Challenges Faced", "Learnings & Key Takeaways", "Future Enhancements", "References"], 2):
    story.append(Paragraph(f"{i}. {t}", B))
story.append(PageBreak())

h1("2. Introduction")
p("Effective learning depends on <b>when</b> material is revised, not only how long it is studied. The forgetting-curve research of "
  "Ebbinghaus showed that memory decays exponentially unless reviewed at growing intervals. <b>StudySprint</b> is a Python application that "
  "brings this idea to everyday students: it stores subjects and topics, records study sessions with a self-rated recall score, and uses the "
  "<b>SM-2 spaced-repetition algorithm</b> to decide when each topic should be revised next. A <b>priority queue (min-heap)</b> ranks "
  "due topics, and a greedy planner fits them into the study time available on a given day. Analytics such as streaks and weak topics give feedback.")
p("The project applies core Python course concepts: functions, classes and dataclasses, modules and packages, exception handling, file and "
  "database I/O (sqlite3), the <font face='Courier'>heapq</font>, <font face='Courier'>datetime</font>, <font face='Courier'>argparse</font>, "
  "<font face='Courier'>logging</font> and <font face='Courier'>csv</font> libraries, list/dict comprehensions, and unit testing with <font face='Courier'>unittest</font>.")

h1("3. Problem Statement")
p("Students revise inconsistently: they forget what they studied, cannot decide which topic to revisit, and have no data about where their time "
  "goes. Generic to-do lists do not model forgetting. <b>Objectives:</b>")
bl(["Provide a simple store for subjects and topics with a difficulty rating.",
    "Record study sessions and self-assessed recall quality.",
    "Automatically compute the next review date of every topic with SM-2.",
    "Produce a prioritised list of due topics and a plan that fits the available time.",
    "Report study time, streaks and weak areas; allow CSV export."])

h1("4. Functional Requirements")
table([["ID", "Module", "Requirement", "Input -> Output"],
       ["FR1", "M1 Subjects & Topics", "Create, read, rename, delete subjects; create, read, update difficulty, delete topics; reject duplicates.", "name/title/difficulty -> stored record or error message"],
       ["FR2", "M2 Session Logging", "Log minutes (1-720), recall quality (0-5) and notes for a topic; list recent sessions.", "topic id, minutes, quality -> session row + new review date"],
       ["FR3", "M3 Scheduler", "Apply SM-2 after each session; list due topics ordered by urgency; build a daily plan within a time budget.", "available minutes -> ordered plan"],
       ["FR4", "M4 Analytics", "Minutes per subject, last-7-day history, current streak, weakest topics, text report, CSV export.", "none -> report text / CSV file"],
       ["FR5", "CLI workflow", "Single command-line entry point with sub-commands and helpful error messages.", "argv -> console output, exit code"]],
      [1.2 * cm, 3.2 * cm, 7 * cm, 5 * cm])
p("<b>User workflow:</b> add subjects/topics -> ask for the daily plan -> study -> log the session with a recall score -> the system reschedules -> "
  "review analytics -> repeat (see workflow diagram).")

story.append(PageBreak()); h1("5. Non-functional Requirements")
table([["Category", "Requirement", "How it is met"],
       ["Performance", "Any command completes in under 1 second for up to 10,000 sessions.", "Indexes on topics.next_review and sessions.topic_id; SQL aggregation."],
       ["Security", "No SQL injection; no secrets stored; input sanitised.", "Parameterised queries only; validators.py checks every input; notes truncated to 500 chars."],
       ["Usability", "Clear commands and human-readable errors, never a stack trace for bad input.", "argparse help, ValidationError caught in cli.main and printed."],
       ["Reliability", "Data stays consistent even if an operation fails.", "Transactions via context manager, foreign keys ON, CHECK constraints."],
       ["Maintainability", "Small single-purpose modules, type hints, docstrings, tests.", "10 modules under studysprint/, 26 unit tests."],
       ["Logging", "Important events and all SQL failures are recorded.", "Rotating file log (logs/studysprint.log)."],
       ["Portability", "Runs on Windows/Linux/macOS with no third-party runtime dependency.", "Standard library only."]],
      [3 * cm, 6.2 * cm, 7.2 * cm])
story.append(PageBreak())

h1("6. System Architecture")
p("StudySprint uses a layered architecture: a thin presentation layer (CLI), a business-logic layer made of four functional modules plus validators, "
  "and a data layer that wraps SQLite. Logging and configuration are cross-cutting concerns. Dependencies point downwards only, so any layer can "
  "be replaced (for example a GUI instead of the CLI) without touching the others.")
img("arch.png", "Figure 1 - System architecture", maxh=15 * cm)

h1("7. Design Diagrams")
h2("7.1 Use Case Diagram"); img("usecase.png", "Figure 2 - Use case diagram", maxh=11 * cm)
h2("7.2 Workflow Diagram"); img("flow.png", "Figure 3 - Workflow of a study cycle", maxh=13 * cm)
story.append(PageBreak())
h2("7.3 Sequence Diagram - logging a session"); img("seq.png", "Figure 4 - Sequence diagram for the 'log' command", maxh=10 * cm)
h2("7.4 Class Diagram"); img("cls.png", "Figure 5 - Class diagram", maxh=12 * cm)
story.append(PageBreak())
h2("7.5 ER Diagram and Schema"); img("er.png", "Figure 6 - ER diagram (SQLite)", maxh=9 * cm)
p("Schema: <b>subjects</b>(id PK, name UNIQUE NOCASE, created_at); <b>topics</b>(id PK, subject_id FK ON DELETE CASCADE, title, difficulty CHECK 1-5, "
  "ease_factor, interval_days, repetitions, next_review, UNIQUE(subject_id,title)); <b>sessions</b>(id PK, topic_id FK ON DELETE CASCADE, minutes CHECK &gt;0, "
  "quality CHECK 0-5, notes, studied_at). Deleting a subject removes its topics and sessions automatically.")

h1("8. Design Decisions & Rationale")
table([["Decision", "Rationale"],
       ["SQLite instead of JSON/CSV files", "Relational integrity (FK, UNIQUE, CHECK), SQL aggregation for analytics, atomic transactions; still zero-install."],
       ["SM-2 algorithm", "Well-known, simple, needs only ease/interval/repetitions per item; easy to unit-test as a pure function."],
       ["Min-heap for due topics", "Priority = (most overdue, hardest, id). A heap gives O(n log n) ordering and shows practical use of a data structure."],
       ["Greedy time-budget planner", "Topics are taken in priority order if they fit the remaining minutes; simple and predictable (a knapsack solver would be over-engineering)."],
       ["Dependency injection (Database passed into each manager)", "Tests use an in-memory database; modules stay decoupled."],
       ["Dates passed as parameters (today=...)", "Makes time-dependent logic (streaks, due dates) deterministic in tests."],
       ["CLI first", "Fastest way to a complete, testable core; the layered design allows a GUI later."]],
      [5.2 * cm, 11.2 * cm])
p("<b>SM-2 rules used:</b> if quality &lt; 3 the repetition count resets and the interval becomes 1 day; otherwise interval = 1 day (1st success), "
  "6 days (2nd) and round(previous interval x ease) afterwards. Ease is updated by EF' = EF + 0.1 - (5-q)(0.08 + (5-q)0.02) and never falls below 1.3.")

h1("9. Implementation Details")
table([["File", "Responsibility"],
       ["main.py", "Entry point calling cli.main()."],
       ["studysprint/config.py", "Paths and constants; environment overrides."],
       ["studysprint/logger.py", "Rotating file logger with safe fallback."],
       ["studysprint/models.py", "Dataclasses Subject, Topic, StudySession."],
       ["studysprint/validators.py", "ValidationError and validate_* functions."],
       ["studysprint/database.py", "SQLite connection, schema creation, execute/query helpers with logging."],
       ["studysprint/subject_manager.py", "Module 1 - CRUD for subjects and topics."],
       ["studysprint/session_tracker.py", "Module 2 - session logging; triggers scheduler."],
       ["studysprint/scheduler.py", "Module 3 - sm2_update(), ReviewScheduler (due_topics with heapq, daily_plan)."],
       ["studysprint/analytics.py", "Module 4 - aggregates, streak, report, CSV export."],
       ["studysprint/cli.py", "argparse sub-commands and error handling."],
       ["tests/", "7 test files covering validators, all modules and an end-to-end CLI flow."]],
      [5.5 * cm, 10.9 * cm])
p("<b>Core code - SM-2 update (scheduler.py):</b>")
for ln in ["def sm2_update(ease, interval, repetitions, quality):",
           "    if quality &lt; 3:                      # failed recall",
           "        repetitions, interval = 0, 1",
           "    else:",
           "        if repetitions == 0:  interval = 1",
           "        elif repetitions == 1: interval = 6",
           "        else: interval = max(1, round(interval * ease))",
           "        repetitions += 1",
           "    ease = ease + 0.1 - (5-quality)*(0.08 + (5-quality)*0.02)",
           "    return max(MIN_EASE, round(ease, 3)), interval, repetitions"]:
    story.append(Paragraph(ln.replace(" ", "&nbsp;"), CODE))
story.append(Spacer(1, 6))
p("<b>Priority queue:</b> each due topic is pushed as <font face='Courier'>(-overdue_days, -difficulty, id, topic)</font> onto a heap and popped in order, "
  "so the most overdue and hardest topics come first. <b>Error handling:</b> validators raise ValidationError, database IntegrityErrors are translated to "
  "friendly messages, and cli.main prints them with exit code 1.")
story.append(PageBreak())

h1("10. Screenshots / Results")
img("shot_setup.png", "Figure 7 - Adding subjects and topics", maxw=14 * cm, maxh=7 * cm)
img("shot_plan.png", "Figure 8 - Due list and 60-minute daily plan (hardest topic first)", maxw=14 * cm, maxh=7 * cm)
img("shot_log.png", "Figure 9 - Logging sessions; SM-2 reschedules (poor recall lowers ease to 2.18)", maxw=15 * cm, maxh=7 * cm)
img("shot_report.png", "Figure 10 - Analytics report and validation error handling", maxw=14 * cm, maxh=13 * cm)
story.append(PageBreak())
h1("11. Testing Approach")
p("Tests use Python's <font face='Courier'>unittest</font> (also runnable with pytest) and an in-memory SQLite database, so they are fast and isolated. "
  "<b>Result: 26 tests, all passing.</b>")
table([["Test file", "What is verified"],
       ["test_validators.py", "Boundaries and invalid types for name, difficulty, quality, minutes, date."],
       ["test_subject_manager.py", "CRUD, case-insensitive duplicate rejection, cascade delete, bad ids."],
       ["test_scheduler.py", "SM-2 interval progression (1, 6, 16), reset on failure, ease floor, priority order, plan never exceeds budget."],
       ["test_session_tracker.py", "Session insert updates next_review and repetitions; invalid inputs rejected; ordering."],
       ["test_analytics.py", "Aggregations, streak (today/yesterday/broken), weakest topic, CSV export, empty database."],
       ["test_cli.py", "End-to-end flow add -> plan -> log -> due -> report, and error propagation."]],
      [5 * cm, 11.4 * cm])
img("shot_tests.png", "Figure 11 - Unit test run", maxw=15 * cm, maxh=11 * cm)

h1("12. Challenges Faced")
bl(["<b>Testing time-dependent logic:</b> streaks and due dates depend on today's date; solved by passing <i>today</i> as an argument.",
    "<b>In-memory SQLite:</b> each new connection creates a fresh database, so one persistent connection is held in the Database class.",
    "<b>Choosing a fair priority:</b> combining overdue days and difficulty into a heap key needed experimentation.",
    "<b>Friendly errors:</b> translating low-level sqlite3.IntegrityError messages into understandable feedback.",
    "<b>Foreign keys:</b> SQLite disables them by default; PRAGMA foreign_keys=ON is required for cascade deletes."])

h1("13. Learnings & Key Takeaways")
bl(["Designing layered, loosely coupled modules makes testing much easier.",
    "Small pure functions (sm2_update) are the easiest and most reliable code to test.",
    "Constraints in the database (CHECK, UNIQUE, FK) act as a second line of defence behind validation.",
    "Using Git commits per module gives a clear development history.",
    "Real algorithms and data structures (SM-2, heap) can be applied to everyday problems."])

h1("14. Future Enhancements")
bl(["Tkinter or web (Flask) front-end with charts.", "Flashcard content per topic and quiz mode.", "Desktop/e-mail reminders for due reviews.",
    "Multi-user accounts and cloud sync.", "Machine-learning model to predict forgetting from session history.", "Export analytics to PDF."])

h1("15. References")
bl(["Wozniak, P. A. (1990). <i>Optimization of learning</i> - the SM-2 algorithm, SuperMemo.",
    "Ebbinghaus, H. (1885). <i>Memory: A Contribution to Experimental Psychology</i>.",
    "Python Software Foundation. Python 3 documentation: sqlite3, heapq, argparse, logging, unittest. https://docs.python.org/3/",
    "SQLite documentation. https://www.sqlite.org/docs.html",
    "Fowler, M. <i>UML Distilled</i>. Addison-Wesley."])


def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
    c.drawCentredString(A4[0] / 2, 1 * cm, f"StudySprint - Project Report - Page {d.page}"); c.restoreState()


SimpleDocTemplate("StudySprint_Project_Report.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                  bottomMargin=1.8 * cm, title="StudySprint Project Report", author="Kirti Yogi").build(story, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("built")
