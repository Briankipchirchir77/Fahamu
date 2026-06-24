from models.person import Person

VALID_COUNTIES = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu", "Machakos",
    "Kajiado", "Muranga", "Nyeri", "Meru", "Embu", "Kitui",
    "Makueni", "Nyandarua", "Laikipia", "Samburu", "Trans Nzoia",
    "Uasin Gishu", "Elgeyo Marakwet", "Nandi", "Baringo", "Kericho",
    "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya",
    "Homa Bay", "Migori", "Kisii", "Nyamira", "Turkana", "West Pokot",
    "Marsabit", "Isiolo", "Garissa", "Wajir", "Mandera",
    "Tana River", "Lamu", "Taita Taveta", "Kwale", "Kilifi",
    "Kirinyaga", "National"
]

class User(Person):
    """A Kenyan citizen who uses Fahamu to stay informed.
    Users consume civic updates and track deadlines — they do NOT create content.
    """
    all_users = []
    id_counter = 1

    def __init__(self, name, email, county="Nairobi", password_hash=""):
        super().__init__(name, email)
        self.id = User.id_counter
        self._county = county
        self.password_hash = password_hash
        self.saved_categories = []   # categories user wants updates for
        self.bookmarked_updates = [] # IDs of updates they saved
        User.id_counter += 1
        User.all_users.append(self)

    @property
    def county(self):
        return self._county

    @county.setter
    def county(self, value):
        if value not in VALID_COUNTIES:
            raise ValueError(f"'{value}' is not a valid Kenyan county")
        self._county = value

    def subscribe_category(self, category):
        if category not in self.saved_categories:
            self.saved_categories.append(category)

    def unsubscribe_category(self, category):
        if category in self.saved_categories:
            self.saved_categories.remove(category)

    def bookmark_update(self, update_id):
        if update_id not in self.bookmarked_updates:
            self.bookmarked_updates.append(update_id)

    def remove_bookmark(self, update_id):
        if update_id in self.bookmarked_updates:
            self.bookmarked_updates.remove(update_id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            "county": self._county,
            "saved_categories": self.saved_categories,
            "bookmarked_updates": self.bookmarked_updates
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            data["name"],
            data["email"],
            data.get("county", "Nairobi"),
            data.get("password_hash", "")
        )
        user.saved_categories = data.get("saved_categories", [])
        user.bookmarked_updates = data.get("bookmarked_updates", [])
        return user

    def __str__(self):
        return f"[{self.id}] {self._name} | {self._email} | {self._county}"

    def __repr__(self):
        return f"User(name={self._name}, county={self._county})"
