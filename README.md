StudySprint - Smart Study Tracker with Spaced Repetition

StudySprint is a Python command-line application for organising subjects and topics, recording study sessions, scheduling revision, and viewing study analytics. It uses the SM-2 spaced-repetition method to calculate review intervals and a priority queue to build a time-limited study plan.

Course: Python Programming - VITyarthi Build Your Own Project
Student: Kirti Yogi
Registration No.: 24MIM10188
Faculty: Ashok Patel
Slots: B21+B22+B23+E14+E21+E22

1. Features

1. Subject and Topic Management - Add, list, and delete subjects/topics with difficulty validation.
2. Study Session Logging - Record study minutes and recall quality from 0 to 5.
3. Smart Scheduler - Calculate review intervals using SM-2 and list due topics using a min-heap.
4. Analytics - Show study totals, recent history, streak information, weak topics, and export sessions to CSV.

The application also includes input validation, error handling, SQLite storage, logging, and automated tests.

2. Requirements

- Python 3.9 or newer
- Git, if cloning the repository
- No GUI is required. The application is designed to run from a terminal.

The application uses Python's standard library. "pytest" is optional; the included test suite can also be run with Python's built-in "unittest" module.

3. Installation

Step 1: Clone the repository

git clone https://github.com/kirtiyogi671-prog/studysprint.git
cd studysprint

Step 2: Create a virtual environment (recommended)

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

Step 3: Install optional test dependency

The application does not require third-party packages to run.

For optional "pytest" support:

python -m pip install -r requirements.txt

If you only want to run the included tests with "unittest", this installation step can be skipped.

4. Configuration

By default, StudySprint stores its SQLite database at:

data/studysprint.db

The database path can be changed with the "STUDYSPRINT_DB" environment variable. The log directory can be changed with "STUDYSPRINT_LOG_DIR".

macOS/Linux:

STUDYSPRINT_DB=demo.db python main.py -h

Windows PowerShell:

$env:STUDYSPRINT_DB="demo.db"
python main.py -h

These variables are optional. No ".env" file or external service is required.

5. Run the Project

First verify that the command-line interface is available:

python main.py -h

Example workflow

python main.py add-subject "Python"
python main.py list-subjects
python main.py add-topic 1 "Decorators" -d 4
python main.py list-topics
python main.py log 1 40 4 -n "solid understanding"
python main.py due
python main.py plan 60
python main.py report
python main.py export sessions.csv

Recall quality is scored from 0 to 5. A score of 5 means perfect recall; lower scores represent more difficulty or forgetting and cause the scheduler to use a shorter review interval.

Try the demonstration data

The repository includes "seed_demo.py", which creates sample data in a separate database file.

macOS/Linux:

STUDYSPRINT_DB=demo.db python scripts/seed_demo.py
STUDYSPRINT_DB=demo.db python main.py report

Windows PowerShell:

$env:STUDYSPRINT_DB="demo.db"
python seed_demo.py
python main.py report

Use an empty database file for the seed script. It will stop if that database already contains data.

6. Command Reference

Command| Purpose
"add-subject NAME"| Add a subject
"list-subjects"| List subjects
"delete-subject ID"| Delete a subject
"add-topic SUBJECT_ID TITLE [-d 1-5]"| Add a topic
"list-topics [-s ID]"| List topics
"delete-topic ID"| Delete a topic
"log TOPIC_ID MINUTES QUALITY [-n NOTES]"| Record a study session
"due"| List topics due for review
"plan MINUTES"| Build a study plan within a time budget
"report"| Show study analytics
"export PATH.csv"| Export study sessions

Run:

python main.py -h

for the complete command-line help.

7. Testing

Run the complete test suite from the repository root:

python -m unittest discover -v

The repository contains automated tests covering the main project modules.

Optional:

pytest -v

8. Project Structure

The project files are stored directly in the repository root:

studysprint/
├── main.py
├── README.md
├── statement.md
├── requirements.txt
├── .gitignore
├── __init__.py
├── config.py
├── logger.py
├── models.py
├── validators.py
├── database.py
├── subject_manager.py
├── session_tracker.py
├── scheduler.py
├── analytics.py
├── cli.py
├── seed_demo.py
├── make_report.py
│
├── test_analytics.py
├── test_cli.py
├── test_scheduler.py
├── test_session_tracker.py
├── test_subject_manager.py
├── test_validators.py
│
├── StudySprint_Project_Report.pdf
│
├── arch.dot
├── arch.png
├── cls.dot
├── cls.png
├── er.png
├── flow.dot
├── flow.png
├── seq.png
├── usecase.dot
├── usecase.png
│
└── screenshots
    ├── shot_setup.png
    ├── shot_log.png
    ├── shot_plan.png
    ├── shot_report.png
    └── shot_tests.png

9. Design and Documentation

The repository includes architecture, workflow, use-case, sequence, class, and ER diagrams along with screenshots demonstrating the project.

The structured project report is available as:

"StudySprint_Project_Report.pdf"

10. Submission

The repository is public for evaluation.

Repository root URL:

https://github.com/kirtiyogi671-prog/studysprint

Submit the repository root URL only.

Do not submit "/tree/main/", "/blob/", or another subdirectory URL.

11. License

The project is submitted as an academic course project for VITyarthi.
