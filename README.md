StudySprint - Smart Study Tracker with Spaced Repetition

StudySprint is a Python command-line study tracker for organising subjects and topics, recording study sessions, scheduling revision, and viewing study analytics. The project uses the SM-2 spaced-repetition approach to calculate review intervals and provides a time-limited study planning feature.

Course: Python Programming - VITyarthi Build Your Own Project
Student: Kirti Yogi
Registration No.: 24MIM10188
Faculty: Ashok Patel
Slots: B21+B22+B23+E14+E21+E22

1. Features

1. Subject and Topic Management - Add, list, and delete subjects and topics.
2. Study Session Logging - Record study time and recall quality from 0 to 5.
3. Smart Scheduler - Calculate review intervals using the SM-2 method and identify topics due for review.
4. Study Planning - Create a study plan within a specified time limit.
5. Analytics - View study totals, recent study history, streak information, and weak topics.
6. CSV Export - Export recorded study sessions to a CSV file.
7. Input Validation - Validate user input and handle invalid values.
8. SQLite Storage - Store application data locally using SQLite.
9. Logging - Maintain application logs.
10. Automated Testing - The repository contains test files for the main project modules.

2. Requirements

- Python 3.9 or newer
- Git, if cloning the repository
- Terminal or Command Prompt

The project is designed as a command-line application and does not require a graphical user interface.

The main application uses Python's standard library. "pytest" is listed in "requirements.txt" for running the test suite.

3. Installation

Step 1: Clone the repository

git clone
https://github.com/kirtiyogi671-prog/studysprint.git
cd studysprint

Step 2: Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

Step 3: Install the listed dependency

python -m pip install -r requirements.txt

4. Configuration

StudySprint uses SQLite for local data storage.

The database path can be configured using the "STUDYSPRINT_DB" environment variable.

macOS/Linux:

STUDYSPRINT_DB=demo.db

Windows PowerShell:

$env:STUDYSPRINT_DB="demo.db"

The logging directory can also be configured using the "STUDYSPRINT_LOG_DIR" environment variable.

5. Main Commands

The project provides commands for managing subjects, topics, study sessions, revision scheduling, planning, reports, and CSV export.

Command| Purpose
"add-subject NAME"| Add a subject
"list-subjects"| List subjects
"delete-subject ID"| Delete a subject
"add-topic SUBJECT_ID TITLE [-d 1-5]"| Add a topic
"list-topics [-s ID]"| List topics
"delete-topic ID"| Delete a topic
"log TOPIC_ID MINUTES QUALITY [-n NOTES]"| Record a study session
"due"| List topics due for review
"plan MINUTES"| Create a study plan
"report"| Display study analytics
"export PATH.csv"| Export study sessions to CSV

Recall quality is recorded on a scale from 0 to 5.

6. Demonstration Data

The repository contains "seed_demo.py", which creates sample subjects, topics, and study sessions for demonstration purposes.

The demonstration script uses the "STUDYSPRINT_DB" environment variable so that sample data can be kept in a separate database file.

macOS/Linux:

STUDYSPRINT_DB=demo.db python seed_demo.py

Windows PowerShell:

$env:STUDYSPRINT_DB="demo.db"
python seed_demo.py

Use an empty database file when creating demonstration data.

7. Testing

The repository contains the following test files:

- "test_analytics.py"
- "test_cli.py"
- "test_scheduler.py"
- "test_session_tracker.py"
- "test_subject_manager.py"
- "test_validators.py"

The tests are written using Python's testing framework and can also be run with "pytest" when it is installed.

pytest -v

8. Project Structure

All current project files are stored directly in the repository root.

studysprint/
├── .gitignore
├── README.md
├── StudySprint_Project_Report.pdf
├── __init__.py
├── analytics.py
├── arch.dot
├── arch.png
├── cli.py
├── cls.dot
├── cls.png
├── config.py
├── database.py
├── er.png
├── flow.dot
├── flow.png
├── logger.py
├── main.py
├── make_report.py
├── models.py
├── requirements.txt
├── scheduler.py
├── seed_demo.py
├── seq.png
├── session_tracker.py
├── shot_log.png
├── shot_plan.png
├── shot_report.png
├── shot_setup.png
├── shot_tests.png
├── statement.md
├── subject_manager.py
├── test_analytics.py
├── test_cli.py
├── test_scheduler.py
├── test_session_tracker.py
├── test_subject_manager.py
├── test_validators.py
├── usecase.dot
├── usecase.png
└── validators.py

9. Documentation

The repository contains the project report:

"StudySprint_Project_Report.pdf"

It also contains architecture, class, flow, sequence, ER, and use-case diagram files, along with project screenshots.

10. GitHub Repository

The project repository is public for evaluation.

Repository:

https://github.com/kirtiyogi671-prog/studysprint

For VITyarthi submission, submit the repository root URL.

Do not submit:

/tree/main/
/blob/main/README.md

Submit only:

https://github.com/kirtiyogi671-prog/studysprint

11. Academic Submission

This project is submitted as an academic project for the VITyarthi Python Programming course.

The repository contains the project source files, documentation, test files, diagrams, demonstration script, and project report.
