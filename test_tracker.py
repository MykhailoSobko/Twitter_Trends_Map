"""Test the tracker module."""

import unittest

from tracker import Tracker
from unittest import TestCase


class TestTracker(TestCase):
    """Test the Tracker class."""

    def setUp(self):
        """Set up the test class."""
        self.tracker = Tracker()

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.tracker.to_track, {})

    def test_get_all_user_trends(self):
        """Test the get_all_user_trends method."""
        self.tracker.get_all_users_trends()
        self.assertNotEqual(self.tracker.to_track, {})

    def test_get_trends_from_api(self):
        """Test the get_trends_from_api method."""
        self.tracker.get_all_users_trends()
        trends = self.tracker.get_trends_from_api()
        self.assertNotEqual(trends, [])

    def test_pass_trends_to_db(self):
        """Test the pass_trends_to_db method."""
        self.tracker.get_all_users_trends()
        trends = self.tracker.get_trends_from_api()
        self.tracker.pass_trends_to_db(trends)
        self.assertNotEqual(self.tracker.to_track, {})


if __name__ == "__main__":
    unittest.main()
