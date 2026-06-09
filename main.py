import argparse
from models.user import User
from models.project import Project
from models.task import Task
from models.update import Update
from models.deadline import Deadline
from utils.file_io import save_to_json, load_from_json
from utils.display import display_users, display_projects, display_tasks, display_updates, display_deadlines

USERS_FILE = "data/users.json"
PROJECTS_FILE = "data/projects.json"
UPDATES_FILE = "data/updates.json"

def main():
    parser = argparse.ArgumentParser(
        prog="fahamu",
        description="🇰🇪 Fahamu — Know What Matters in Kenya"
    )
    subparsers = parser.add_subparsers(dest="command")

    # add-user
    p = subparsers.add_parser("add-user", help="Register a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--county", default="Nairobi")

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    # add-project
    p = subparsers.add_parser("add-project", help="Add a project")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", required=True)

    # list-projects
    p = subparsers.add_parser("list-projects", help="List projects")
    p.add_argument("--user", default=None)

    # add-task
    p = subparsers.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", required=True)

    # complete-task
    p = subparsers.add_parser("complete-task", help="Mark a task complete")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)

    # list-tasks
    p = subparsers.add_parser("list-tasks", help="List tasks for a project")
    p.add_argument("--project", required=True)

    # add-update
    p = subparsers.add_parser("add-update", help="Add a critical update")
    p.add_argument("--title", required=True)
    p.add_argument("--category", required=True)
    p.add_argument("--county", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--date", required=True)

    # list-updates
    p = subparsers.add_parser("list-updates", help="View updates")
    p.add_argument("--county", default=None)
    p.add_argument("--category", default=None)

    # list-deadlines
    subparsers.add_parser("list-deadlines", help="View government deadlines")

    args = parser.parse_args()

    # ── Handlers ──

    if args.command == "add-user":
        user = User(args.name, args.email, args.county)
        users = load_from_json(USERS_FILE)
        users.append(user.to_dict())
        save_to_json(users, USERS_FILE)
        print(f"✅ User '{args.name}' added!")

    elif args.command == "list-users":
        users = load_from_json(USERS_FILE)
        display_users(users)

    elif args.command == "add-project":
        project = Project(args.title, args.description, args.due_date, args.user)
        projects = load_from_json(PROJECTS_FILE)
        projects.append(project.to_dict())
        save_to_json(projects, PROJECTS_FILE)
        print(f"✅ Project '{args.title}' added!")

    elif args.command == "list-projects":
        projects = load_from_json(PROJECTS_FILE)
        if args.user:
            projects = [p for p in projects if p["user_name"].lower() == args.user.lower()]
        display_projects(projects)

    elif args.command == "add-task":
        projects = load_from_json(PROJECTS_FILE)
        found = False
        for p in projects:
            if p["title"].lower() == args.project.lower():
                task = Task(args.title, args.assigned_to, args.project)
                p["tasks"].append(task.to_dict())
                found = True
                break
        if found:
            save_to_json(projects, PROJECTS_FILE)
            print(f"✅ Task '{args.title}' added to '{args.project}'!")
        else:
            print(f"❌ Project '{args.project}' not found.")

    elif args.command == "complete-task":
        projects = load_from_json(PROJECTS_FILE)
        found = False
        for p in projects:
            if p["title"].lower() == args.project.lower():
                for t in p["tasks"]:
                    if t["title"].lower() == args.task.lower():
                        t["status"] = "complete"
                        found = True
                        break
        if found:
            save_to_json(projects, PROJECTS_FILE)
            print(f"✅ Task '{args.task}' marked complete!")
        else:
            print(f"❌ Task '{args.task}' not found in '{args.project}'.")

    elif args.command == "list-tasks":
        projects = load_from_json(PROJECTS_FILE)
        for p in projects:
            if p["title"].lower() == args.project.lower():
                display_tasks(p.get("tasks", []))
                return
        print(f"❌ Project '{args.project}' not found.")

    elif args.command == "add-update":
        update = Update(args.title, args.category, args.county, args.description, args.date)
        updates = load_from_json(UPDATES_FILE)
        updates.append(update.to_dict())
        save_to_json(updates, UPDATES_FILE)
        print(f"✅ Update '{args.title}' added!")

    elif args.command == "list-updates":
        updates = load_from_json(UPDATES_FILE)
        if args.county:
            updates = [u for u in updates if u["county"].lower() == args.county.lower()]
        if args.category:
            updates = [u for u in updates if u["category"].lower() == args.category.lower()]
        display_updates(updates)

    elif args.command == "list-deadlines":
        from datetime import date
        deadlines = [
            Deadline("KRA Tax Returns", date(2026, 6, 30), "File your income tax returns", "KRA"),
            Deadline("NTSA License Renewal", date(2026, 6, 14), "Renew your driving licence", "NTSA"),
        ]
        display_deadlines(deadlines)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()