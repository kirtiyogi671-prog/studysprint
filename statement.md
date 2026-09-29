# Problem Statement
Students revise inconsistently: they forget what they studied, cannot tell which topic to revisit, and have no
data about how their time is spent. Generic to-do apps do not model forgetting.

## Scope
A local Python application that (1) stores subjects/topics, (2) records study sessions with a self-rated recall score,
(3) schedules the next review per topic using SM-2 and plans a day within a time budget, and (4) reports study analytics.
Out of scope: multi-user accounts, cloud sync, GUI/mobile apps, flashcard content.

## Target Users
School and college students, competitive-exam aspirants and self-learners who study several subjects.

## High-Level Features
- Subject and topic CRUD with difficulty ratings
- Study session logging with recall quality
- SM-2 spaced-repetition scheduling and priority-queue "due" list
- Time-budgeted daily plan
- Analytics: totals, streak, 7-day history, weak topics, CSV export
