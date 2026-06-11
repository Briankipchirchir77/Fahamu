from datetime import date

# Deadline tracks government due dates like KRA returns or NTSA renewals
# days_remaining is calculated dynamically using today's date

class Deadline:
    all_deadlines = []

    def __init__(self, title, due_date, description, source):
        self.title = title
        self._due_date = due_date  # expects a datetime.date object
        self.description = description
        self.source = source  # e.g. "KRA", "NTSA"
        Deadline.all_deadlines.append(self)

    # calculated property - no need to store this, just compute on the fly
    @property
    def days_remaining(self):
        return (self._due_date - date.today()).days

    # anything within a week counts as urgent
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
        urgency = "URGENT" if self.is_urgent else "upcoming"
        return f"[{urgency}] {self.title} - {self.days_remaining} days left"
