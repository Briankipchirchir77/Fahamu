import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def _path(filename):
    return os.path.join(DATA_DIR, filename)

def save_to_json(data, filepath):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_from_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: Corrupted data in {filepath}")
        return []

# Convenience helpers for each data type
def load_updates():
    return load_from_json(_path("updates.json"))

def save_updates(updates):
    return save_to_json(updates, _path("updates.json"))

def load_deadlines():
    return load_from_json(_path("deadlines.json"))

def save_deadlines(deadlines):
    return save_to_json(deadlines, _path("deadlines.json"))

def load_users():
    return load_from_json(_path("users.json"))

def save_users(users):
    return save_to_json(users, _path("users.json"))
