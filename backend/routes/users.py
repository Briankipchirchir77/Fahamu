from flask import Blueprint, jsonify, request
from utils.file_io import load_users, save_users

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    users = load_users()
    return jsonify(users)

@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    for field in ["name", "email"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    users = load_users()
    # prevent duplicate emails
    if any(u.get("email") == data["email"] for u in users):
        return jsonify({"error": "Email already registered"}), 409

    new_id = max((u.get("id", 0) for u in users), default=0) + 1
    new_user = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"],
        "county": data.get("county", "Nairobi"),
        "saved_categories": data.get("saved_categories", []),
        "bookmarked_updates": []
    }
    users.append(new_user)
    save_users(users)
    return jsonify(new_user), 201

@users_bp.route("/<int:user_id>/categories", methods=["PUT"])
def update_categories(user_id):
    users = load_users()
    user = next((u for u in users if u.get("id") == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    user["saved_categories"] = data.get("categories", [])
    save_users(users)
    return jsonify(user)

@users_bp.route("/<int:user_id>/bookmarks", methods=["PUT"])
def update_bookmarks(user_id):
    users = load_users()
    user = next((u for u in users if u.get("id") == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    update_id = data.get("update_id")
    action = data.get("action", "add")
    bookmarks = user.get("bookmarked_updates", [])
    if action == "add" and update_id not in bookmarks:
        bookmarks.append(update_id)
    elif action == "remove" and update_id in bookmarks:
        bookmarks.remove(update_id)
    user["bookmarked_updates"] = bookmarks
    save_users(users)
    return jsonify(user)

@users_bp.route("/counties", methods=["GET"])
def get_counties():
    return jsonify([
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu",
        "Machakos", "Kajiado", "Muranga", "Nyeri", "Meru",
        "Embu", "Kitui", "Makueni", "Uasin Gishu", "Kericho",
        "Kakamega", "Bungoma", "Homa Bay", "Migori", "Kisii",
        "Turkana", "Garissa", "Mombasa", "Lamu", "Taita Taveta",
        "Kirinyaga", "National"
    ])
