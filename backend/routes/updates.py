from flask import Blueprint, jsonify, request
from utils.file_io import load_updates, save_updates
from datetime import date

updates_bp = Blueprint("updates", __name__)

@updates_bp.route("/", methods=["GET"])
def get_updates():
    """Get all civic updates, with optional filters."""
    updates = load_updates()
    category = request.args.get("category")
    county   = request.args.get("county")

    if category:
        updates = [u for u in updates if u.get("category") == category]
    if county:
        updates = [u for u in updates if u.get("county") in (county, "National")]

    # Sort newest first
    updates.sort(key=lambda u: u.get("published_date", ""), reverse=True)
    return jsonify(updates)

@updates_bp.route("/<int:update_id>", methods=["GET"])
def get_update(update_id):
    updates = load_updates()
    update = next((u for u in updates if u.get("id") == update_id), None)
    if not update:
        return jsonify({"error": "Update not found"}), 404
    return jsonify(update)

@updates_bp.route("/", methods=["POST"])
def create_update():
    """Admin only: create a new civic update."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    required = ["title", "category", "county", "summary"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    updates = load_updates()
    new_id = max((u.get("id", 0) for u in updates), default=0) + 1
    new_update = {
        "id": new_id,
        "title": data["title"],
        "category": data["category"],
        "county": data["county"],
        "summary": data["summary"],
        "source_url": data.get("source_url", ""),
        "published_date": data.get("published_date", str(date.today())),
        "admin_name": data.get("admin_name", "admin")
    }
    updates.append(new_update)
    save_updates(updates)
    return jsonify(new_update), 201

@updates_bp.route("/<int:update_id>", methods=["PUT"])
def edit_update(update_id):
    """Admin only: edit an existing update."""
    updates = load_updates()
    update = next((u for u in updates if u.get("id") == update_id), None)
    if not update:
        return jsonify({"error": "Update not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    for key in ["title", "category", "county", "summary", "source_url"]:
        if key in data:
            update[key] = data[key]

    save_updates(updates)
    return jsonify(update)

@updates_bp.route("/<int:update_id>", methods=["DELETE"])
def delete_update(update_id):
    """Admin only: delete an update."""
    updates = load_updates()
    new_list = [u for u in updates if u.get("id") != update_id]
    if len(new_list) == len(updates):
        return jsonify({"error": "Update not found"}), 404
    save_updates(new_list)
    return jsonify({"deleted": update_id})

@updates_bp.route("/categories", methods=["GET"])
def get_categories():
    return jsonify([
        "tax", "health", "education", "transport", "land",
        "water", "security", "elections", "business"
    ])
