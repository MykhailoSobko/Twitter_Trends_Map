<<<<<<< HEAD
=======
"""
Api key: Qe5JCyirsxF8Bm7NxRUxnYElo
Api secret: XdcfwjYkr3fHbFTYlZnGA8Q4oLttY8DFzKFpkbb8GEwXWkACpK

Bearer token: 

Access token: 1099616859274600449-2e6lBnIzgOxOPCDWCOVCwKgr84Vhol
Access secret: mtHovZ3sUvCvoxaClMnyySoDqMsUjcNdsOWqeaAbYQpOz
"""

>>>>>>> dd0b77e (Initial commit)
import json
import requests
from pprint import pprint

<<<<<<< HEAD
bearer_token = "BEARER TOKEN"
=======
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFENNAEAAAAAv64mN0Pv8NhUZXJW4%2BYfJrCfbTY%3DV7sARtRzvCflWL2iK1wAfTYrwLaQe9cZ55IdwX32dFmIKlC4Qx"
>>>>>>> dd0b77e (Initial commit)


def get_place_woeid(country=None, city=None, path='place_woeids.json'):
    '''Get woeid parameter for forming request to trends API.
    If country is specified, return its woeid, if country and city are None,
    return Worldwide woeid which equals to 1'''
    if not country and not city:
        return 1

    # look for woeids in a ready file
    with open(path, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)

    countries = {item['name']:item['woeid'] for item in data if item['placeType']['code']==12}
    if country:
        if country in countries:
            woeid = countries[country]
            return woeid
        else:
            return None
    
    # if city is given
    if city:
        cities = {item['name']:item['woeid'] for item in data if item['placeType']['code']==7 and item['parentid']==woeid}
        if city in cities:
            woeid = cities[city]
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


if __name__ == '__main__':
    trends = get_json('United Kingdom')
    pprint(trends)