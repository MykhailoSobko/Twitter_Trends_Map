from unittest import TestCase
import api_work


class TestApiWork(TestCase):
    '''doc'''

    def test_get_place_woeid(self):
        '''doc'''
        country_0 = ''
        city_0 = ''
        country_1 = 'Ukraine'
        city_1 = 'Lviv'
        country_2 = 'hbshbdhsbhebhebjkdejhbdj'
        city_2 = 'London'
        country_3 = 30
        city_3 = list('12,34,45,5')
        self.assertEqual(api_work.get_place_woeid(), 1)
        self.assertEqual(api_work.get_place_woeid(country_0, city_0), 1)
        self.assertEqual(api_work.get_place_woeid(country_0, city_1), None)
        self.assertEqual(api_work.get_place_woeid(country_1, city_1), 924943)
        self.assertEqual(api_work.get_place_woeid(country_2, city_2), None)
        self.assertEqual(api_work.get_place_woeid(country_3, city_3), None)
        self.assertEqual(api_work.get_place_woeid(country_1, city_0), 23424976)
        self.assertEqual(api_work.get_place_woeid(country_1, city_2), None)
        self.assertEqual(api_work.get_place_woeid(country_1, city_3), None)
        self.assertEqual(api_work.get_place_woeid(country_0, city_3), None)

    def test_get_json(self):
        '''doc'''
        self.assertEqual(type(api_work.get_json('Ukraine')), type(api_work.get_json()),  type(api_work.get_json('')))
        self.assertEqual(type(api_work.get_json('country')), type(api_work.get_json('Ukraine', 'Warsaw')))
        self.assertEqual(type((api_work.get_json('Ukraine')['trends'])), list)
        self.assertEqual(type((api_work.get_json('Ukraine')['trends'][0])), dict)
        self.assertEqual(type((api_work.get_json('Ukraine')['trends'][0]['name'])), str)
