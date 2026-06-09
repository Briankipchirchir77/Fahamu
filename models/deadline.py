from datetime import date

class Deadline:
    all_deadlines = []

    def __init__(self, title, due_date, description, source):
        self.title = title
        self._due_date = due_date
        self.description = description
        self.source = source
        Deadline.all_deadlines.append(self)

    @property
    def days_remaining(self):
        return (self._due_date - date.today()).days

    @property
    def is_urgent(self):
        return self.days_remaining <= 7

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": str(self._due_date),
            "description": self.description,
            "source": self.source
        }

    def __str__(self):
        urgency = "⚠️ URGENT" if self.is_urgent else "📋"
        return f"{urgency} {self.title} — {self.days_remaining} days left"