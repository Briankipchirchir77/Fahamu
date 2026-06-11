# Task belongs to a project
# status is locked to three values only - setter enforces this

class Task:
    all_tasks = []
    id_counter = 1

    def __init__(self, title, assigned_to, project_title, status="pending"):
        self.id = Task.id_counter
        self._title = title
        self._status = status
        self.assigned_to = assigned_to
        self.project_title = project_title
        Task.id_counter += 1
        Task.all_tasks.append(self)

    @property
    def title(self):
        return self._title

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        # reject anything thats not one of these three
        if value not in ["pending", "in_progress", "complete"]:
            raise ValueError("Status must be: pending, in_progress, or complete")
        self._status = value

    def complete(self):
        # shortcut so you can just call task.complete() instead of setting status manually
        self._status = "complete"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self._title,
            "status": self._status,
            "assigned_to": self.assigned_to,
            "project_title": self.project_title
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["assigned_to"],
            data["project_title"],
            data["status"]
        )

    def __str__(self):
        icon = "done" if self._status == "complete" else "in progress" if self._status == "in_progress" else "pending"
        return f"[{self.id}] {self._title} | Assigned: {self.assigned_to} | {icon}"

    def __repr__(self):
        return f"Task(title={self._title}, status={self._status})"
