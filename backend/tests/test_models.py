import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.user import User
from models.admin import Admin
from models.deadline import Deadline
from models.civic_update import CivicUpdate
from datetime import date, timedelta


class TestUser(unittest.TestCase):
    def setUp(self):
        User.all_users.clear()
        User.id_counter = 1
        self.user = User("Wanjiku", "wanjiku@email.com", "Nairobi")

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Wanjiku")
        self.assertEqual(self.user.county, "Nairobi")

    def test_invalid_county(self):
        with self.assertRaises(ValueError):
            self.user.county = "Wakanda"

    def test_valid_county(self):
        self.user.county = "Mombasa"
        self.assertEqual(self.user.county, "Mombasa")

    def test_subscribe_category(self):
        self.user.subscribe_category("tax")
        self.assertIn("tax", self.user.saved_categories)

    def test_no_duplicate_subscription(self):
        self.user.subscribe_category("tax")
        self.user.subscribe_category("tax")
        self.assertEqual(len(self.user.saved_categories), 1)

    def test_unsubscribe_category(self):
        self.user.subscribe_category("health")
        self.user.unsubscribe_category("health")
        self.assertNotIn("health", self.user.saved_categories)

    def test_bookmark_update(self):
        self.user.bookmark_update(5)
        self.assertIn(5, self.user.bookmarked_updates)

    def test_no_duplicate_bookmark(self):
        self.user.bookmark_update(5)
        self.user.bookmark_update(5)
        self.assertEqual(len(self.user.bookmarked_updates), 1)

    def test_remove_bookmark(self):
        self.user.bookmark_update(5)
        self.user.remove_bookmark(5)
        self.assertNotIn(5, self.user.bookmarked_updates)

    def test_to_dict(self):
        d = self.user.to_dict()
        self.assertEqual(d["name"], "Wanjiku")
        self.assertIn("bookmarked_updates", d)

    def test_from_dict(self):
        d = self.user.to_dict()
        u2 = User.from_dict(d)
        self.assertEqual(u2.name, "Wanjiku")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.user.name = ""

    def test_user_str(self):
        self.assertIn("Wanjiku", str(self.user))


class TestAdmin(unittest.TestCase):
    def setUp(self):
        Admin.all_admins.clear()
        Admin.id_counter = 1
        self.admin = Admin("Kamau", "kamau@fahamu.ke", role="superadmin")

    def test_admin_creation(self):
        self.assertEqual(self.admin.name, "Kamau")
        self.assertEqual(self.admin.role, "superadmin")

    def test_is_superadmin(self):
        self.assertTrue(self.admin.is_superadmin)

    def test_editor_not_superadmin(self):
        editor = Admin("Otieno", "otieno@fahamu.ke", role="editor")
        self.assertFalse(editor.is_superadmin)

    def test_to_dict_hides_password(self):
        self.admin.password_hash = "secret"
        d = self.admin.to_dict()
        self.assertNotIn("password_hash", d)


class TestDeadline(unittest.TestCase):
    def setUp(self):
        Deadline.all_deadlines.clear()
        Deadline.id_counter = 1
        future = date.today() + timedelta(days=30)
        self.deadline = Deadline("KRA Returns", future, "File on iTax", "KRA", "tax")

    def test_days_remaining(self):
        self.assertGreater(self.deadline.days_remaining, 0)

    def test_not_urgent(self):
        self.assertFalse(self.deadline.is_urgent)

    def test_urgent_within_week(self):
        soon = date.today() + timedelta(days=3)
        d = Deadline("NTSA", soon, "Renew licence", "NTSA", "transport")
        self.assertTrue(d.is_urgent)

    def test_overdue(self):
        past = date.today() - timedelta(days=5)
        d = Deadline("Old deadline", past, "Missed", "KRA", "tax")
        self.assertTrue(d.is_overdue)
        self.assertEqual(d.status, "overdue")

    def test_to_dict(self):
        d = self.deadline.to_dict()
        self.assertIn("days_remaining", d)
        self.assertIn("status", d)

    def test_from_dict(self):
        d = self.deadline.to_dict()
        d2 = Deadline.from_dict(d)
        self.assertEqual(d2.title, "KRA Returns")


class TestCivicUpdate(unittest.TestCase):
    def setUp(self):
        CivicUpdate.all_updates.clear()
        CivicUpdate.id_counter = 1
        self.update = CivicUpdate(
            "New Health Insurance Rules",
            "health",
            "National",
            "NHIF has updated its contribution tiers for 2026.",
            "https://nhif.or.ke",
            admin_name="Kamau"
        )

    def test_update_creation(self):
        self.assertEqual(self.update.title, "New Health Insurance Rules")
        self.assertEqual(self.update.category, "health")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            self.update.category = "sports"

    def test_to_dict(self):
        d = self.update.to_dict()
        self.assertEqual(d["category"], "health")
        self.assertIn("source_url", d)

    def test_from_dict(self):
        d = self.update.to_dict()
        u2 = CivicUpdate.from_dict(d)
        self.assertEqual(u2.title, "New Health Insurance Rules")

    def test_str(self):
        self.assertIn("HEALTH", str(self.update))


if __name__ == "__main__":
    unittest.main()
