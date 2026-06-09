from rich.console import Console
from rich.table import Table

console = Console()

def display_users(users):
    table = Table(title="👤 Registered Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Email", style="green")
    table.add_column("County", style="yellow")
    for u in users:
        table.add_row(str(u.get("id", "")), u["name"], u["email"], u["county"])
    console.print(table)

def display_projects(projects):
    table = Table(title="📁 Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Owner", style="green")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="magenta")
    for p in projects:
        table.add_row(
            str(p.get("id", "")), p["title"], p["user_name"],
            p["due_date"], str(len(p.get("tasks", [])))
        )
    console.print(table)

def display_tasks(tasks):
    table = Table(title="✅ Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Assigned To", style="green")
    table.add_column("Status", style="yellow")
    for t in tasks:
        table.add_row(str(t.get("id", "")), t["title"], t["assigned_to"], t["status"])
    console.print(table)

def display_updates(updates):
    table = Table(title="🇰🇪 Fahamu — Latest Updates")
    table.add_column("Category", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("County", style="green")
    table.add_column("Date", style="yellow")
    for u in updates:
        table.add_row(u["category"].upper(), u["title"], u["county"], u["date"])
    console.print(table)

def display_deadlines(deadlines):
    table = Table(title="📋 Upcoming Government Deadlines")
    table.add_column("Title", style="white")
    table.add_column("Days Left", style="red")
    table.add_column("Description", style="yellow")
    for d in deadlines:
        table.add_row(d.title, str(d.days_remaining), d.description)
    console.print(table)