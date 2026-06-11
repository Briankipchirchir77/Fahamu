# Project belongs to a user and holds a list of tasks

class Project:
    all_projects = []
    id_counter = 1

    def __init__(self, title, description, due_date, user_name):
        self.id = Project.id_counter
        self._title = title
        self.description = description
        self.due_date = due_date
        self.user_name = user_name
        self.tasks = []
        Project.id_counter += 1
        Project.all_projects.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        self._title = value

    def add_task(self, task):
        self.tasks.append(task)

    def completed_tasks(self):
        # list comprehension - filters tasks that are done
        return [t for t in self.tasks if t.status == "complete"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self._title,
            "description": self.description,
            "due_date": self.due_date,
            "user_name": self.user_name,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        # import inside method to avoid circular import between project and task
        from models.task import Task
        project = cls(
            data["title"],
            data["description"],
            data["due_date"],
            data["user_name"]
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project

    def __str__(self):
        return f"[{self.id}] {self._title} | Owner: {self.user_name} | Due: {self.due_date} | Tasks: {len(self.tasks)}"

    def __repr__(self):
        return f"Project(title={self._title}, user={self.user_name})"
