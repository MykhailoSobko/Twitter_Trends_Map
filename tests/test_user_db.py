"""Test the user_db module."""

import unittest

from user_db import User, Authenticator
from unittest import TestCase


class TestUser(TestCase):
    """Test the User class."""

    def setUp(self) -> None:
        """Set up the test class."""
        self.user = User("user", "password")

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.user.username, "user")
        self.assertEqual(self.user.password, "password")
        self.assertIsNone(self.user.logged_in)

    def test_check_password(self):
        """Test the check_password method."""
        self.assertTrue(self.user.check_password("password"))
        self.assertFalse(self.user.check_password("wrong"))

    def test_add_user(self):
        """Test the add_user method."""
        self.user.add_user()

    def test_logout(self):
        """Test the logout method."""
        self.user.logout()
        self.assertFalse(self.user.logged_in)

    def test_add_trend_to_track(self):
        """Test the add_trend_to_track method."""
        self.user.add_trend_to_track("Music", "Ukraine")

    def test_get_all_info_for_user(self):
        """Test the get_all_info_for_user method."""
        tr_info, deleted = self.user.get_all_info_for_user("user")
        self.assertNotEqual(tr_info, [])
        self.assertNotEqual(deleted, [])

    def test_check_trend_growth(self):
        """Test the check_trend_growth method."""
        growth = self.user.check_trend_growth({"analytics": {1: 100, 2: 200}})
        self.assertEqual(growth, 1.0)

    def test_add_track_trend_to_db(self):
        """Test the _add_track_trend_to_db method."""
        self.user._add_track_trend_to_db("Music", "Ukraine")

    def test_delete_trend_from_tracked(self):
        """Test the delete_trend_from_tracked method."""
        self.user._add_track_trend_to_db("Music", "Ukraine")
        self.user.delete_trend_from_tracked("Music", "Ukraine")


class TestAuthenticator(TestCase):
    """Test the Authenticator class."""

    def setUp(self) -> None:
        """Set up the test class."""
        self.authenticator = Authenticator()

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.authenticator.users, {})
        self.assertIsNone(self.authenticator.current_user)

    def test_register(self):
        """Test the register method."""
        self.authenticator.register("user", "password")

    def test_user_exists(self):
        """Test the user_exists method."""
        self.authenticator.register("user", "password")
        self.assertTrue(self.authenticator.user_exists("user"))

    def test_login(self):
        """Test the login method."""
        self.authenticator.register("user", "password")
        self.authenticator.login("user", "password")

    def test_is_logged_in(self):
        """Test the is_logged_in method."""
        self.authenticator.register("user", "password")
        self.authenticator.login("user", "password")
        self.authenticator.is_logged_in("user")


if __name__ == "__main__":
    unittest.main()
