"""
Testing module.
"""

import unittest
from unittest import TestCase
from trends_adt import Trend, TrendsADT
from api_work import get_json


class TrendTest(TestCase):
    """
    Class to test a Trend class.
    """

    def test_trend(self):
        trends = get_json('United Kingdom')
        trend_object = Trend(trends, "12.05.2021", "United Kingdom")
        self.assertEqual(trend_object.location, "United Kingdom")
        self.assertEqual(trend_object.added_at, "12.05.2021")


class TrendsADTTest(TestCase):
    """
    Class to test Trends ADT.
    """

    def test_trends_adt(self):
        trends_adt = TrendsADT()
        self.assertEqual(trends_adt.get_trend_from_db('#RCBvKKR', 'Worldwide'), None)
        with self.assertRaises(TypeError):
            get_item_from_trend = trends_adt.get_trend_from_db('#RCBvKKR', 'Worldwide')[0]


if __name__ == '__main__':
    unittest.main()
