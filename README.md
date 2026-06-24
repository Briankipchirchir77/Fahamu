# Fahamu — Civic Intelligence for Kenyans

**Fahamu** (Swahili: *to understand*) is a civic information platform that keeps Kenyans informed on tax deadlines, government services, health updates, and county-level civic news.

## Architecture

```
fahamu/
├── backend/               Flask REST API
│   ├── app.py             Entry point — registers all blueprints
│   ├── models/
│   │   ├── person.py      Base class (name, email, validation)
│   │   ├── user.py        Citizen — reads updates, bookmarks, subscribes
│   │   ├── admin.py       Admin — creates/edits/deletes content only
│   │   ├── civic_update.py Content object (title, category, county, summary)
│   │   └── deadline.py    Government deadline with live days_remaining
│   ├── routes/
│   │   ├── updates.py     CRUD for civic updates (admin-write, public-read)
│   │   ├── deadlines.py   CRUD for deadlines + seeded KRA/NTSA/SHA data
│   │   ├── users.py       User registration, category subscriptions, bookmarks
│   │   └── external.py    Proxy: NewsAPI, forex rates, eCitizen service links
│   ├── utils/file_io.py   JSON persistence helpers
│   ├── data/              Runtime JSON files (auto-created)
│   └── tests/test_models.py  28 unit tests — all pass
│
└── frontend/              React SPA (single HTML file, zero build step)
    └── index.html         Full app — runs standalone or against Flask API
```

## Key Design Decisions

- **Admins create, users consume.** The old `Project` / `Task` model was replaced with `CivicUpdate` (admin-authored) and `Deadline` (admin-managed). Users only browse, filter, bookmark, and subscribe.
- **`days_remaining` is always computed live** — never stored — so it's always accurate.
- **Frontend works offline** with seed data, and automatically upgrades to live API data when Flask is running.

## Running Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py          # starts on http://localhost:5000

# Frontend
open frontend/index.html   # or serve with any static server
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/updates/?category=tax&county=Nairobi | List civic updates |
| POST | /api/updates/ | Create update (admin) |
| PUT | /api/updates/:id | Edit update (admin) |
| DELETE | /api/updates/:id | Delete update (admin) |
| GET | /api/deadlines/?status=urgent | List deadlines |
| POST | /api/deadlines/ | Add deadline (admin) |
| GET | /api/external/news?category=tax | Kenya civic news |
| GET | /api/external/ecitizen-services | eCitizen portal links |
| GET | /api/external/forex | KES exchange rates |

## Admin Access
Default demo PIN: **1234** — change in `frontend/index.html` before production.
