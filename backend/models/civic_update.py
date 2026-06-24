from datetime import date

VALID_CATEGORIES = ["tax", "health", "education", "transport", "land", "water", "security", "elections", "business"]

class CivicUpdate:
    """Represents a civic update or alert published by an admin.
    Users browse these — they do not create them.
    """
    all_updates = []
    id_counter = 1

    def __init__(self, title, category, county, summary, source_url, published_date=None, admin_name="admin"):
        self.id = CivicUpdate.id_counter
        self._title = title
        self._category = category  # e.g. "tax", "health"
        self.county = county       # "National" or a specific county
        self.summary = summary
        self.source_url = source_url
        self.published_date = published_date or str(date.today())
        self.admin_name = admin_name
        CivicUpdate.id_counter += 1
        CivicUpdate.all_updates.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(f"'{value}' is not a valid category. Choose from: {VALID_CATEGORIES}")
        self._category = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self._title,
            "category": self._category,
            "county": self.county,
            "summary": self.summary,
            "source_url": self.source_url,
            "published_date": self.published_date,
            "admin_name": self.admin_name
        }

    @classmethod
    def from_dict(cls, data):
        update = cls(
            data["title"],
            data["category"],
            data["county"],
            data["summary"],
            data.get("source_url", ""),
            data.get("published_date"),
            data.get("admin_name", "admin")
        )
        return update

    def __str__(self):
        return f"[{self._category.upper()}] {self._title} | {self.county} | {self.published_date}"

    def __repr__(self):
        return f"CivicUpdate(title={self._title}, category={self._category})"
