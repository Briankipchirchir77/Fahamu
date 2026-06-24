import argparse
from models.user import User
from models.admin import Admin
from models.civic_update import CivicUpdate
from models.deadline import Deadline
from utils.file_io import save_to_json, load_from_json, _path
from utils.display import display_users, display_updates, display_deadlines

USERS_FILE = _path("users.json")
UPDATES_FILE = _path("updates.json")
DEADLINES_FILE = _path("deadlines.json")


# fix for id_counter bug - reads existing JSON and finds the highest id
# so new entries continue from where we left off instead of starting at 1
def get_next_id(filepath):
    data = load_from_json(filepath)
    if not data:
        return 1
    ids = [item["id"] for item in data if "id" in item]
    return max(ids) + 1 if ids else 1


def main():
    parser = argparse.ArgumentParser(
        prog="fahamu",
        description="Fahamu - Know What Matters in Kenya"
    )
    subparsers = parser.add_subparsers(dest="command")

    # ── User commands (citizens) ──────────────────────────────────────────
    p = subparsers.add_parser("add-user", help="Register a new citizen user")
    p.add_argument("--name",   required=True)
    p.add_argument("--email",  required=True)
    p.add_argument("--county", default="Nairobi")

    subparsers.add_parser("list-users", help="List all registered users")

    p = subparsers.add_parser("subscribe", help="Subscribe a user to a category")
    p.add_argument("--email",    required=True)
    p.add_argument("--category", required=True)

    # ── Civic update commands (admin only) ────────────────────────────────
    p = subparsers.add_parser("add-update", help="[Admin] Publish a civic update")
    p.add_argument("--title",       required=True)
    p.add_argument("--category",    required=True,
                   choices=["tax","health","education","transport",
                            "land","water","security","elections","business"])
    p.add_argument("--county",      required=True)
    p.add_argument("--summary",     required=True)
    p.add_argument("--source-url",  default="")
    p.add_argument("--admin",       default="admin")

    p = subparsers.add_parser("list-updates", help="View civic updates")
    p.add_argument("--county",   default=None)
    p.add_argument("--category", default=None)

    p = subparsers.add_parser("delete-update", help="[Admin] Remove a civic update by ID")
    p.add_argument("--id", required=True, type=int)

    # ── Deadline commands (admin only) ────────────────────────────────────
    p = subparsers.add_parser("add-deadline", help="[Admin] Add a government deadline")
    p.add_argument("--title",       required=True)
    p.add_argument("--due-date",    required=True, help="Format: YYYY-MM-DD")
    p.add_argument("--description", default="")
    p.add_argument("--source",      required=True,
                   choices=["KRA","NTSA","SHA","NSSF","eCitizen",
                            "Huduma","County","IEBC","CAK","Other"])
    p.add_argument("--category",    default="tax",
                   choices=["tax","health","education","transport",
                            "land","water","security","elections","business"])
    p.add_argument("--county",      default="National")

    subparsers.add_parser("list-deadlines", help="View all government deadlines")

    p = subparsers.add_parser("delete-deadline", help="[Admin] Remove a deadline by ID")
    p.add_argument("--id", required=True, type=int)

    args = parser.parse_args()

    # ── Handlers ──────────────────────────────────────────────────────────

    if args.command == "add-user":
        User.id_counter = get_next_id(USERS_FILE)
        user = User(args.name, args.email, args.county)
        users = load_from_json(USERS_FILE)
        users.append(user.to_dict())
        save_to_json(users, USERS_FILE)
        print(f"✓ User '{args.name}' registered in {args.county}.")

    elif args.command == "list-users":
        users = load_from_json(USERS_FILE)
        if not users:
            print("No users registered yet.")
        else:
            display_users(users)

    elif args.command == "subscribe":
        users = load_from_json(USERS_FILE)
        matched = False
        for u in users:
            if u["email"].lower() == args.email.lower():
                cats = u.get("saved_categories", [])
                if args.category not in cats:
                    cats.append(args.category)
                    u["saved_categories"] = cats
                    matched = True
                else:
                    print(f"'{args.email}' is already subscribed to '{args.category}'.")
                    return
        if matched:
            save_to_json(users, USERS_FILE)
            print(f"✓ '{args.email}' subscribed to '{args.category}'.")
        else:
            print(f"No user found with email '{args.email}'.")

    elif args.command == "add-update":
        updates = load_from_json(UPDATES_FILE)
        new_id = get_next_id(UPDATES_FILE)
        from datetime import date
        new_update = {
            "id":             new_id,
            "title":          args.title,
            "category":       args.category,
            "county":         args.county,
            "summary":        args.summary,
            "source_url":     args.source_url,
            "published_date": str(date.today()),
            "admin_name":     args.admin
        }
        updates.append(new_update)
        save_to_json(updates, UPDATES_FILE)
        print(f"✓ Update '{args.title}' published under [{args.category}].")

    elif args.command == "list-updates":
        updates = load_from_json(UPDATES_FILE)
        if args.county:
            updates = [u for u in updates if u["county"].lower() == args.county.lower()
                       or u["county"].lower() == "national"]
        if args.category:
            updates = [u for u in updates if u["category"].lower() == args.category.lower()]
        if not updates:
            print("No updates found for that filter.")
        else:
            display_updates(updates)

    elif args.command == "delete-update":
        updates = load_from_json(UPDATES_FILE)
        new_list = [u for u in updates if u.get("id") != args.id]
        if len(new_list) == len(updates):
            print(f"No update found with ID {args.id}.")
        else:
            save_to_json(new_list, UPDATES_FILE)
            print(f"✓ Update {args.id} deleted.")

    elif args.command == "add-deadline":
        deadlines = load_from_json(DEADLINES_FILE)
        new_id = get_next_id(DEADLINES_FILE)
        new_deadline = {
            "id":          new_id,
            "title":       args.title,
            "due_date":    args.due_date,
            "description": args.description,
            "source":      args.source,
            "category":    args.category,
            "county":      args.county
        }
        deadlines.append(new_deadline)
        save_to_json(deadlines, DEADLINES_FILE)
        print(f"✓ Deadline '{args.title}' added (due {args.due_date}).")

    elif args.command == "list-deadlines":
        deadlines = load_from_json(DEADLINES_FILE)
        if not deadlines:
            print("No deadlines found.")
        else:
            display_deadlines(deadlines)

    elif args.command == "delete-deadline":
        deadlines = load_from_json(DEADLINES_FILE)
        new_list = [d for d in deadlines if d.get("id") != args.id]
        if len(new_list) == len(deadlines):
            print(f"No deadline found with ID {args.id}.")
        else:
            save_to_json(new_list, DEADLINES_FILE)
            print(f"✓ Deadline {args.id} deleted.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()