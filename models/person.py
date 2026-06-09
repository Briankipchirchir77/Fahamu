class Person:
    def __init__(self, name, email):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email

    def __repr__(self):
        return f"Person(name={self._name})"