from flask import Blueprint, jsonify, request
from datetime import date, datetime

deadlines_bp = Blueprint("deadlines", __name__)

# In-memory seed data — in production this would load from file_io
SEED_DEADLINES = [
    {
        "id": 1, "title": "KRA Individual Tax Returns", "due_date": "2026-06-30",
        "description": "File your income tax return for the year 2025 on iTax portal.",
        "source": "KRA", "category": "tax", "county": "National"
    },
    {
        "id": 2, "title": "NHIF Annual Compliance", "due_date": "2026-07-15",
        "description": "Employers must ensure all staff are registered and contributions up to date.",
        "source": "NHIF", "category": "health", "county": "National"
    },
    {
        "id": 3, "title": "NTSA Vehicle Inspection", "due_date": "2026-08-01",
        "description": "All PSV vehicles must undergo mandatory annual inspection.",
        "source": "NTSA", "category": "transport", "county": "National"
    },
    {
        "id": 4, "title": "Business Permit Renewal — Nairobi", "due_date": "2026-06-20",
        "description": "Annual business permit renewal for Nairobi County businesses.",
        "source": "County", "category": "business", "county": "Nairobi"
    },
    {
        "id": 5, "title": "NSSF Contribution Filing", "due_date": "2026-07-09",
        "description": "Monthly NSSF contribution returns due by 9th of each month.",
        "source": "NSSF", "category": "tax", "county": "National"
    },
]

def _days_remaining(due_date_str):
    try:
        d = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        return (d - date.today()).days
    except Exception:
        return None

def _enrich(deadline):
    days = _days_remaining(deadline["due_date"])
    deadline["days_remaining"] = days
    if days is None:
        deadline["status"] = "unknown"
    elif days < 0:
        deadline["status"] = "overdue"
    elif days <= 7:
        deadline["status"] = "urgent"
    else:
        deadline["status"] = "upcoming"
    return deadline

from utils.file_io import load_deadlines, save_deadlines

def _get_all():
    stored = load_deadlines()
    if not stored:
        # seed on first run
        save_deadlines(SEED_DEADLINES)
        return [_enrich(dict(d)) for d in SEED_DEADLINES]
    return [_enrich(dict(d)) for d in stored]

@deadlines_bp.route("/", methods=["GET"])
def get_deadlines():
    deadlines = _get_all()
    category = request.args.get("category")
    county   = request.args.get("county")
    status   = request.args.get("status")

    if category:
        deadlines = [d for d in deadlines if d.get("category") == category]
    if county:
        deadlines = [d for d in deadlines if d.get("county") in (county, "National")]
    if status:
        deadlines = [d for d in deadlines if d.get("status") == status]

    deadlines.sort(key=lambda d: d.get("days_remaining") or 9999)
    return jsonify(deadlines)

@deadlines_bp.route("/", methods=["POST"])
def create_deadline():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    required = ["title", "due_date", "description", "source"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    stored = load_deadlines()
    if not stored:
        stored = list(SEED_DEADLINES)

    new_id = max((d.get("id", 0) for d in stored), default=0) + 1
    new_deadline = {
        "id": new_id,
        "title": data["title"],
        "due_date": data["due_date"],
        "description": data["description"],
        "source": data["source"],
        "category": data.get("category", "tax"),
        "county": data.get("county", "National")
    }
    stored.append(new_deadline)
    save_deadlines(stored)
    return jsonify(_enrich(new_deadline)), 201

@deadlines_bp.route("/<int:deadline_id>", methods=["DELETE"])
def delete_deadline(deadline_id):
    stored = load_deadlines() or list(SEED_DEADLINES)
    new_list = [d for d in stored if d.get("id") != deadline_id]
    if len(new_list) == len(stored):
        return jsonify({"error": "Deadline not found"}), 404
    save_deadlines(new_list)
    return jsonify({"deleted": deadline_id})
