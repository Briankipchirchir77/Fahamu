# base class for anyone who uses the system
# User inherits from this so i dont repeat name/email logic everywhere

class Person:
    def __init__(self, name, email):
        # using underscore prefix means these are meant to be private
        # we access them through properties below
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    # this setter makes sure nobody passes an empty string as a name
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
