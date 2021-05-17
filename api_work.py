import json
import requests
from pprint import pprint

bearer_token = "BEARER TOKEN REMOVED"


def get_place_woeid(country=None, city=None, path='place_woeids.json'):
    '''Get woeid parameter for forming request to trends API.
    If country is specified, return its woeid, if country and city are None,
    return Worldwide woeid which equals to 1'''    
    # look for woeids in a ready file
    with open(path, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    
    if not country:
        woeid = 1
    else:
         woeid = None

    countries = {item['name']:item['woeid'] for item in data if item['placeType']['code']==12}
    
    if type(country)==str:
        if country in countries:
            woeid = countries[country]    

    # if city is given
    if city and woeid:
        cities = {item['name']:item['woeid'] for item in data if item['placeType']['code']==7 and item['parentid']==woeid}
        if type(city)==str and city in cities:
            woeid = cities[city]
        elif city:
            return None

    return woeid


def get_json(country=None, city=None):
    """
    Sends request to Twitter Trends API based on the given country.
    Returns list with trend objects for the country.
    Struecture of return:
    """
    place_woeid = get_place_woeid(country, city)
    if place_woeid:
        base_url = f"https://api.twitter.com/1.1/trends/place.json?id={place_woeid}"
    else:
        return None

    search_headers = {
        "Authorization": f'Bearer {bearer_token}'
    }
    response = requests.get(base_url, headers=search_headers)
    return response.json()[0]
