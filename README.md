# Fahamu — Know What Matters in Kenya

Fahamu is a command line tool that helps Kenyans stay informed and organised. It tracks civic updates like power outages, water cuts, fuel prices and government deadlines — and provides a project and task manager for individuals and small teams.

The name comes from the Swahili word meaning "to know" or "to understand."

---

## The Problem

Kenya has 47 counties each dealing with daily crises — power outages, water cuts, fuel price changes, road closures, government deadlines. The information exists but it is scattered. By the time most Kenyans find out about a planned outage, their food has already spoiled. By the time they remember a KRA deadline, the fine has already hit.

Fahamu brings all of that into one place.

---

## Features

- Register users with county-based filtering
- Create and manage projects with due dates
- Add tasks to projects and mark them complete
- Track civic updates by category — umeme, maji, mafuta, barabara, serikali, hali ya hewa
- Filter updates by county or category
- View government deadlines with live days remaining and urgency alerts
- Fully offline — works without internet on any machine
- Data stored locally in JSON files

---

## Supported Counties

- Nairobi
- Mombasa
- Kisumu
- Nakuru

---

## Tech Stack

- Python 3
- argparse — CLI commands
- rich — terminal tables and display
- Pipenv — dependency management
- JSON — local data storage
- unittest — unit testing
- coverage — test coverage reporting

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Briankipchirchir77/Fahamu.git
cd Fahamu
```

Install dependencies using Pipenv:

```bash
pip install pipenv
pipenv install
pipenv shell
```

Or using pip directly:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Fahamu/
├── main.py               # entry point — all CLI commands live here
├── models/
│   ├── __init__.py       # makes models a Python package
│   ├── person.py         # base class with name and email
│   ├── user.py           # inherits from Person, adds county and categories
│   ├── project.py        # belongs to a user, holds tasks
│   ├── task.py           # belongs to a project, has status
│   ├── update.py         # civic alerts by category and county
│   └── deadline.py       # government deadlines with days remaining
├── utils/
│   ├── __init__.py       # makes utils a Python package
│   ├── file_io.py        # save and load JSON helpers
│   └── display.py        # rich table display functions
├── data/
│   ├── users.json        # stored users
│   ├── projects.json     # stored projects and tasks
│   └── updates.json      # stored civic updates
├── tests/
│   ├── __init__.py       # makes tests a Python package
│   └── test_models.py    # unit tests for all models
├── Pipfile
├── requirements.txt
└── README.md
```

---

## Usage

### Users

```bash
# add a new user
python main.py add-user --name "Brian Otieno" --email "brian@gmail.com" --county "Nairobi"

# list all users
python main.py list-users
```

### Projects

```bash
# add a project
python main.py add-project --user "Brian Otieno" --title "Fahamu App" --due-date "2026-12-31"

# list all projects
python main.py list-projects

# filter by user
python main.py list-projects --user "Brian Otieno"
```

### Tasks

```bash
# add a task to a project
python main.py add-task --project "Fahamu App" --title "Build CLI" --assigned-to "Brian Otieno"

# mark a task complete
python main.py complete-task --project "Fahamu App" --task "Build CLI"

# list tasks for a project
python main.py list-tasks --project "Fahamu App"
```

### Civic Updates

```bash
# add an update
python main.py add-update --title "Westlands Blackout" --category "umeme" --county "Nairobi" --description "KPLC maintenance on Waiyaki Way" --date "2026-06-13"

# list all updates
python main.py list-updates

# filter by county
python main.py list-updates --county "Nairobi"

# filter by category
python main.py list-updates --category "umeme"
```

### Deadlines

```bash
# view government deadlines with days remaining
python main.py list-deadlines
```

---

## Update Categories

| Category | Meaning |
|---|---|
| umeme | Power outages |
| maji | Water cuts |
| mafuta | Fuel prices |
| barabara | Road updates |
| serikali | Government notices |
| hali_ya_hewa | Weather alerts |

---

## Running Tests

```bash
pipenv run python -m unittest tests.test_models -v
```

### Test Coverage

```bash
pipenv run coverage run -m unittest tests.test_models -v
pipenv run coverage report -m
```

Current coverage: 95%+

---

## OOP Concepts Used

- **Inheritance** — User extends Person, getting name and email for free
- **Encapsulation** — private attributes with controlled getters and setters
- **Polymorphism** — each model has its own to_dict and from_dict implementation
- **Class variables** — all_users, id_counter shared across instances
- **Properties** — controlled access to private attributes with validation

---

## Roadmap

- Connect to Kenya Power API for live outage data
- OpenWeatherMap integration for county weather alerts
- Expand to all 47 counties
- SMS alerts via Africa's Talking API
- Web version using Flask and PostgreSQL
- Mobile app

---

## The Vision

Fahamu starts as a terminal tool but the architecture is already designed to scale. The same models that power the CLI will power a future web API — you just swap the argparse layer for Flask routes. The vision is a platform every Kenyan opens before leaving the house.

---

## Author

Brian Kipchirchir — [github.com/Briankipchirchir77](https://github.com/Briankipchirchir77)