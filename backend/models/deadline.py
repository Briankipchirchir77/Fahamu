from datetime import date

VALID_SOURCES = ["KRA", "NTSA", "NSSF", "NHIF", "eCitizen", "Huduma", "County", "IEBC", "CAK", "Other"]

class Deadline:
    """Tracks government deadlines like KRA returns, NTSA renewals, etc.
    Created and managed by admins. Users subscribe to categories to get relevant ones.
    days_remaining is calculated dynamically — never stored.
    """
    all_deadlines = []
    id_counter = 1

    def __init__(self, title, due_date, description, source, category="tax", county="National"):
        self.id = Deadline.id_counter
        self.title = title
        self._due_date = due_date  # expects a datetime.date object or "YYYY-MM-DD" string
        self.description = description
        self.source = source        # e.g. "KRA", "NTSA"
        self.category = category    # maps to civic categories
        self.county = county        # "National" or specific county
        Deadline.id_counter += 1
        Deadline.all_deadlines.append(self)

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        # accept both date objects and strings
        if isinstance(value, str):
            from datetime import datetime
            self._due_date = datetime.strptime(value, "%Y-%m-%d").date()
        else:
            self._due_date = value

    @property
    def days_remaining(self):
        if isinstance(self._due_date, str):
            from datetime import datetime
            d = datetime.strptime(self._due_date, "%Y-%m-%d").date()
        else:
            d = self._due_date
        return (d - date.today()).days

    @property
    def is_urgent(self):
        # within a week counts as urgent
        return 0 <= self.days_remaining <= 7

    @property
    def is_overdue(self):
        return self.days_remaining < 0

    @property
    def status(self):
        if self.is_overdue:
            return "overdue"
        if self.is_urgent:
            return "urgent"
        return "upcoming"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": str(self._due_date),
            "description": self.description,
            "source": self.source,
            "category": self.category,
            "county": self.county,
            "days_remaining": self.days_remaining,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["due_date"],
            data["description"],
            data["source"],
            data.get("category", "tax"),
            data.get("county", "National")
        )

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} — {self.days_remaining} days left ({self.source})"

    def __repr__(self):
        return f"Deadline(title={self.title}, source={self.source}, due={self._due_date})"
