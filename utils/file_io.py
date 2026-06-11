import json
import os

# two functions - one saves to JSON, one loads from JSON
# all data lives in the data/ folder

def save_to_json(data, filepath):
    try:
        # create the data/ folder if it doesnt exist yet
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
        # normal on first run - file doesnt exist yet
        return []
    except json.JSONDecodeError:
        print(f"Warning: Corrupted data in {filepath}")
        return []
