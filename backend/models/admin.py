from models.person import Person

class Admin(Person):
    """Admin is the only one who creates, edits, and deletes civic updates and deadlines.
    Users only read. Admins write.
    """
    all_admins = []
    id_counter = 1

    def __init__(self, name, email, password_hash="", role="editor"):
        super().__init__(name, email)
        self.id = Admin.id_counter
        self.password_hash = password_hash
        self.role = role  # "editor" or "superadmin"
        Admin.id_counter += 1
        Admin.all_admins.append(self)

    @property
    def is_superadmin(self):
        return self.role == "superadmin"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            "role": self.role
            # password_hash intentionally omitted from serialization
        }

    @classmethod
    def from_dict(cls, data):
        admin = cls(
            data["name"],
            data["email"],
            data.get("password_hash", ""),
            data.get("role", "editor")
        )
        return admin

    def __str__(self):
        return f"[ADMIN:{self.role}] {self._name} | {self._email}"

    def __repr__(self):
        return f"Admin(name={self._name}, role={self.role})"
