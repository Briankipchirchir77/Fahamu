class Update:
    CATEGORIES = ["umeme", "maji", "mafuta", "serikali", "barabara", "hali_ya_hewa"]
    all_updates = []

    def __init__(self, title, category, county, description, date):
        self._title = title
        self._category = category
        self._county = county
        self.description = description
        self.date = date
        Update.all_updates.append(self)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in Update.CATEGORIES:
            raise ValueError(f"Invalid category. Choose from {Update.CATEGORIES}")
        self._category = value

    def to_dict(self):
        return {
            "title": self._title,
            "category": self._category,
            "county": self._county,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"], data["category"],
            data["county"], data["description"], data["date"]
        )

    def __str__(self):
        return f"[{self._category.upper()}] {self._title} | {self._county} | {self.date}"

    def __repr__(self):
        return f"Update(title={self._title}, category={self._category})"