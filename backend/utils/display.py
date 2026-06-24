"""
display.py — Rich terminal output for Fahamu CLI use.
All functions accept lists of dicts (from JSON) or model objects.
Run `python display.py` to see a demo with seed data.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from datetime import date

console = Console(width=None)


def display_updates(updates: list):
    """Print a formatted table of civic updates."""
    table = Table(
        title="📢 Fahamu — Civic Updates",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold white on dark_green"
    )
    table.add_column("ID",        style="dim cyan",    no_wrap=True)
    table.add_column("Category",  style="bold yellow", no_wrap=True)
    table.add_column("Title",     style="white",       ratio=3)
    table.add_column("County",    style="green",       no_wrap=True)
    table.add_column("Published", style="dim white",   no_wrap=True)
    table.add_column("Admin",     style="dim cyan",    no_wrap=True)

    for u in updates:
        table.add_row(
            str(u.get("id", "")),
            u.get("category", "").upper(),
            u.get("title", ""),
            u.get("county", ""),
            u.get("published_date", ""),
            u.get("admin_name", "")
        )
    console.print(table)


def display_deadlines(deadlines):
    """
    Print a formatted table of government deadlines.
    Accepts either Deadline model objects or plain dicts.
    Highlights urgent deadlines in red, overdue in dim.
    """
    table = Table(
        title="⏰ Fahamu — Government Deadlines",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold white on dark_red"
    )
    table.add_column("Status",      width=10, no_wrap=True)
    table.add_column("Days Left",   width=10, justify="right", no_wrap=True)
    table.add_column("Title",       width=35)
    table.add_column("Source",      width=8,  no_wrap=True)
    table.add_column("Due Date",    width=12, no_wrap=True)
    table.add_column("Description", width=40)

    for d in deadlines:
        # support both objects and dicts
        if hasattr(d, "days_remaining"):
            days = d.days_remaining
            status = d.status
            title = d.title
            source = d.source
            due = str(d._due_date)
            desc = d.description
        else:
            from datetime import datetime
            try:
                due_dt = datetime.strptime(d.get("due_date", ""), "%Y-%m-%d").date()
                days = (due_dt - date.today()).days
            except Exception:
                days = None
            status = ("overdue" if days is not None and days < 0
                      else "urgent" if days is not None and days <= 7
                      else "upcoming")
            title = d.get("title", "")
            source = d.get("source", "")
            due = d.get("due_date", "")
            desc = d.get("description", "")

        days_str = ("OVERDUE" if days is not None and days < 0
                    else "TODAY" if days == 0
                    else f"{days} days" if days is not None else "?")

        if status == "urgent":
            status_text = Text("⚠ URGENT", style="bold red")
            days_style = "bold red"
        elif status == "overdue":
            status_text = Text("✗ OVERDUE", style="dim red")
            days_style = "dim red"
        else:
            status_text = Text("● upcoming", style="green")
            days_style = "green"

        table.add_row(status_text, Text(days_str, style=days_style), title, source, due, desc)

    console.print(table)


def display_users(users: list):
    """Print a formatted table of registered users."""
    table = Table(
        title="👤 Fahamu — Registered Users",
        box=box.ROUNDED,
        header_style="bold white on dark_blue"
    )
    table.add_column("ID",          style="dim cyan",   width=4)
    table.add_column("Name",        style="white",      width=18)
    table.add_column("Email",       style="green",      width=28)
    table.add_column("County",      style="yellow",     width=14)
    table.add_column("Subscribed",  style="dim white",  width=30)

    for u in users:
        cats = ", ".join(u.get("saved_categories", [])) or "—"
        table.add_row(
            str(u.get("id", "")),
            u.get("name", ""),
            u.get("email", ""),
            u.get("county", ""),
            cats
        )
    console.print(table)


def display_summary(updates: list, deadlines: list):
    """Print a summary dashboard panel — useful for CLI health checks."""
    from datetime import datetime

    urgent = 0
    for d in deadlines:
        if hasattr(d, "days_remaining"):
            days = d.days_remaining
        else:
            try:
                due = datetime.strptime(d.get("due_date", ""), "%Y-%m-%d").date()
                days = (due - date.today()).days
            except Exception:
                continue
        if 0 <= days <= 7:
            urgent += 1

    text = (
        f"[bold green]Civic Updates:[/bold green]  {len(updates)}\n"
        f"[bold yellow]Deadlines:[/bold yellow]      {len(deadlines)}\n"
        f"[bold red]Urgent (≤7 days):[/bold red] {urgent}\n\n"
        f"[dim]Last checked: {date.today().strftime('%d %b %Y')}[/dim]"
    )
    console.print(Panel(text, title="[bold]Fahamu — Dashboard Summary[/bold]", border_style="green", width=50))


# ── Demo mode ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from utils.file_io import load_updates, load_deadlines, load_users

    updates   = load_updates()
    deadlines = load_deadlines()
    users     = load_users()

    display_summary(updates, deadlines)
    console.print()
    display_updates(updates)
    console.print()
    display_deadlines(deadlines)
    console.print()
    if users:
        display_users(users)
    else:
        console.print("[dim]No users registered yet.[/dim]")