from models.person import Person

class User(Person):
    all_users = []
    id_counter = 1

    def __init__(self, name, email, county="Nairobi"):
        super().__init__(name, email)
        self.id = User.id_counter
        self._county = county
        self.saved_categories = []
        User.id_counter += 1
        User.all_users.append(self)

    @property
    def county(self):
        return self._county

    @county.setter
    def county(self, value):
        valid_counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru"]
        if value not in valid_counties:
            raise ValueError(f"{value} is not a valid county")
        self._county = value

    def add_category(self, category):
        if category not in self.saved_categories:
            self.saved_categories.append(category)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            "county": self._county,
            "saved_categories": self.saved_categories
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"], data["email"], data["county"])
        user.saved_categories = data.get("saved_categories", [])
        return user

    def __str__(self):
        return f"[{self.id}] {self._name} | {self._email} | {self._county}"

    def __repr__(self):
        return f"User(name={self._name}, county={self._county})"