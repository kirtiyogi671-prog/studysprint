StudySprint - Smart Study Tracker with Spaced Repetition

StudySprint is a Python command-line application for organising subjects and topics, recording study sessions, scheduling revision, and viewing study analytics. It uses the SM-2 spaced-repetition method to calculate review intervals and helps create a time-limited study plan.

Course: Python Programming - VITyarthi Build Your Own Project
Student: Kirti Yogi
Registration No.: 24MIM10188
Faculty: Ashok Patel
Slots: B21+B22+B23+E14+E21+E22

1. Features

1. Subject and Topic Management - Add, list, and delete subjects and topics.
2. Study Session Logging - Record study time and recall quality from 0 to 5.
3. Smart Scheduler - Calculate review intervals using the SM-2 method and identify topics due for review.
4. Analytics - View study totals, recent history, streak information, weak topics, and export sessions to CSV.
5. Input Validation - Validate user input and handle invalid values.
6. SQLite Storage - Store study data locally using SQLite.
7. Logging - Maintain application logs.
8. Automated Testing - Includes test files for the main project modules.

2. Requirements

- Python 3.9 or newer
- Git, if cloning the repository
- Terminal or Command Prompt

The application is designed to run from the command line and does not require a graphical user interface.

The project uses Python's standard library for runtime functionality. "pytest" is included as an optional testing dependency.

3. Installation

Step 1: Clone the repository

git clone https://github.com/kirtiyogi671-prog/studysprint.git
cd studysprint

Step 2: Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

Step 3: Install the optional testing dependency

python -m pip install -r requirements.txt

The application itself uses Python's standard library.

4. Run the Project

Check the command-line interface with:

python main.py -h

Example commands:

python main.py add-subject "Python"
python main.py list-subjects
python main.py add-topic 1 "Decorators" -d 4
python main.py list-topics
python main.py log 1 40 4 -n "solid understanding"
python main.py due
python main.py plan 60
python main.py report
python main.py export sessions.csv

Recall quality is entered on a scale from 0 to 5 and is used by the scheduler when calculating review intervals.

5. Demonstration Data

The repository contains "seed_demo.py", which can be used to create sample study data.

macOS/Linux:

STUDYSPRINT_DB=demo.db python seed_demo.py
STUDYSPRINT_DB=demo.db python main.py report

Windows PowerShell:

$env:STUDYSPRINT_DB="demo.db"
python seed_demo.py
python main.py report

Use an empty database file for demonstration data.

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
"plan MINUTES"| Build a study plan within a time limit
"report"| Display study analytics
"export PATH.csv"| Export study sessions to CSV

For complete command-line help:

python main.py -h

7. Testing

The repository contains automated test files for the project modules.

Run the tests with Python's built-in "unittest":

python -m unittest discover -v

If "pytest" is installed, the tests can also be run with:

pytest -v

8. Project Structure

The project files are currently stored directly in the repository root.

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

The repository contains the project report and diagrams used for documentation.

The project report is:

"StudySprint_Project_Report.pdf"

Architecture, class, flow, sequence, ER, and use-case diagrams are also included in the repository.

10. GitHub Submission

The repository is public for evaluation.

Repository URL:

https://github.com/kirtiyogi671-prog/studysprint

Submit the repository root URL to VITyarthi.

Do not submit a "/tree/main/", "/blob/main/", or individual file URL.

11. Academic Submission

This project is submitted as an academic project for the VITyarthi Python Programming course.

The repository contains the project source files, documentation, automated tests, diagrams, demonstration script, and project report.
