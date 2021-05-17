import json
import unittest
from copy import deepcopy
from trends_adt import TrendsADT, Trend


class TestTrendsADT(unittest.TestCase):
    def setUp(self):
        trends_json = open("trends.json")
        self.trends_dict = json.load(trends_json)
        self.trends_dict_raw = deepcopy(self.trends_dict)
        trends_json.close()

        self.trends_adt = TrendsADT(self.trends_dict)

    def test_constructor(self):
        self.assertEqual(self.trends_adt.as_of, "2021-04-28T12:06:56Z")
        self.assertEqual(self.trends_adt.location, "Worldwide")
        self.assertEqual(len(self.trends_adt._trends), 4)
        self.assertEqual(type(self.trends_adt._trends[0]).__name__, 'dict')

    def test_getitem(self):
        self.assertEqual(self.trends_adt[0], {'name': '#桃鈴ねね3D',
                                              'added_at': '2021-04-28T12:06:56Z',
                                              'country': 'Worldwide',
                                              'analytics': {'2021-04-28T12:06:56Z': 68151}})

    def test_iter(self):
        for trend in self.trends_adt:
            self.assertEqual(type(trend).__name__, 'dict')

    def test_Trend_filter(self):
        raw_trend = self.trends_dict_raw[0]['trends'][0]
        self.assertEqual(raw_trend, {
            "name": "#桃鈴ねね3D",
            "url": "http://twitter.com/search?q=%23%E6%A1%83%E9%88%B4%E3%81%AD%E3%81%AD3D",
            "promoted_content": None,
            "query": "%23%E6%A1%83%E9%88%B4%E3%81%AD%E3%81%AD3D",
            "tweet_volume": 68151
        })

        self.assertEqual(Trend(raw_trend, '2021-04-28T12:06:56Z', 'Worldwide').filter_trend(),
                         {'name': '#桃鈴ねね3D',
                          'added_at': '2021-04-28T12:06:56Z',
                          'country': 'Worldwide',
                          'analytics': {'2021-04-28T12:06:56Z': 68151}})


unittest.main()
