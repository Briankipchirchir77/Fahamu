# 🇰🇪 Fahamu — Know What Matters

A Python CLI tool for managing users, projects, tasks and critical Kenyan updates.

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/fahamu
cd fahamu
pip install -r requirements.txt
```

## CLI Commands

```bash
# Users
python main.py add-user --name "Brian" --email "brian@email.com" --county "Nairobi"
python main.py list-users

# Projects
python main.py add-project --user "Brian" --title "Fahamu App" --due-date "2026-12-01"
python main.py list-projects --user "Brian"

# Tasks
python main.py add-task --project "Fahamu App" --title "Build CLI" --assigned-to "Brian"
python main.py complete-task --project "Fahamu App" --task "Build CLI"
python main.py list-tasks --project "Fahamu App"

# Updates
python main.py add-update --title "Westlands Blackout" --category umeme --county Nairobi --date "2026-06-11"
python main.py list-updates --county Nairobi

# Deadlines
python main.py list-deadlines
```

## Running Tests

```bash
python -m pytest tests/
```