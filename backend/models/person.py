class Person:
    """Base class for anyone with an identity in the system.
    User and Admin both inherit from this.
    """
    def __init__(self, name, email):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Invalid email address")
        self._email = value.lower().strip()

    def __repr__(self):
        return f"Person(name={self._name}, email={self._email})"
