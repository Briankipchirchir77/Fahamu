import unittest
from models.user import User
from models.project import Project
from models.task import Task

# tests for the three main models
# setUp runs before each test so we start with a clean state every time

class TestUser(unittest.TestCase):
    def setUp(self):
        # clear class-level lists before each test to avoid leftover data
        User.all_users.clear()
        User.id_counter = 1
        self.user = User("Brian", "brian@email.com", "Nairobi")

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Brian")
        self.assertEqual(self.user.county, "Nairobi")

    def test_invalid_county(self):
        # Eldoret is not in the valid list, should raise ValueError
        with self.assertRaises(ValueError):
            self.user.county = "Eldoret"

    def test_add_category(self):
        self.user.add_category("umeme")
        self.assertIn("umeme", self.user.saved_categories)

    def test_duplicate_category(self):
        # adding same category twice should only store it once
        self.user.add_category("umeme")
        self.user.add_category("umeme")
        self.assertEqual(len(self.user.saved_categories), 1)

    def test_to_dict(self):
        d = self.user.to_dict()
        self.assertEqual(d["name"], "Brian")

    def test_from_dict(self):
        # serialize then deserialize - should get same data back
        d = self.user.to_dict()
        u2 = User.from_dict(d)
        self.assertEqual(u2.name, "Brian")

    def test_name_setter(self):
        # name can be changed through the setter
        self.user.name = "Alice"
        self.assertEqual(self.user.name, "Alice")

    def test_empty_name_raises(self):
        # empty name should not be allowed
        with self.assertRaises(ValueError):
            self.user.name = ""

    def test_user_str(self):
        result = str(self.user)
        self.assertIn("Brian", result)

    def test_user_repr(self):
        result = repr(self.user)
        self.assertIn("Brian", result)


class TestProject(unittest.TestCase):
    def setUp(self):
        Project.all_projects.clear()
        Project.id_counter = 1
        Task.all_tasks.clear()
        Task.id_counter = 1
        self.project = Project("Fahamu", "Kenya app", "2026-12-01", "Brian")

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Fahamu")
        self.assertEqual(self.project.user_name, "Brian")

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            self.project.title = ""

    def test_add_task(self):
        task = Task("Build CLI", "Brian", "Fahamu")
        self.project.add_task(task)
        self.assertEqual(len(self.project.tasks), 1)

    def test_completed_tasks(self):
        task = Task("Build CLI", "Brian", "Fahamu")
        task.complete()
        self.project.add_task(task)
        # should return only the one completed task
        self.assertEqual(len(self.project.completed_tasks()), 1)

    def test_to_dict(self):
        d = self.project.to_dict()
        self.assertEqual(d["title"], "Fahamu")

    def test_from_dict(self):
        # convert to dict and back, should get same data
        d = self.project.to_dict()
        p2 = Project.from_dict(d)
        self.assertEqual(p2.title, "Fahamu")

    def test_project_str(self):
        result = str(self.project)
        self.assertIn("Fahamu", result)

    def test_project_repr(self):
        result = repr(self.project)
        self.assertIn("Fahamu", result)


class TestTask(unittest.TestCase):
    def setUp(self):
        Task.all_tasks.clear()
        Task.id_counter = 1
        self.task = Task("Write README", "Brian", "Fahamu")

    def test_default_status(self):
        # new tasks should start as pending
        self.assertEqual(self.task.status, "pending")

    def test_complete_task(self):
        self.task.complete()
        self.assertEqual(self.task.status, "complete")

    def test_invalid_status(self):
        # "done" is not one of the allowed values
        with self.assertRaises(ValueError):
            self.task.status = "done"

    def test_to_dict(self):
        d = self.task.to_dict()
        self.assertEqual(d["title"], "Write README")

    def test_from_dict(self):
        # serialize then deserialize - should get same data back
        d = self.task.to_dict()
        t2 = Task.from_dict(d)
        self.assertEqual(t2.title, "Write README")

    def test_task_str(self):
        result = str(self.task)
        self.assertIn("Write README", result)

    def test_task_repr(self):
        result = repr(self.task)
        self.assertIn("Write README", result)

    def test_in_progress_status(self):
        # make sure in_progress is also a valid status
        self.task.status = "in_progress"
        self.assertEqual(self.task.status, "in_progress")


if __name__ == "__main__":
    unittest.main()
