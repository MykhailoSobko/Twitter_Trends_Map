import requests
import json

def get_json():
    """
    Function sends request to Twitter Api and gets .json object with information about current trends in Twitter.
    """
    base_url = "https://api.twitter.com/1.1/trends/place.json?id=1"
    bearer_token = "BEARER TOKEN WAS REMOVED DUE TO SAFETY REASONS"

    search_headers = {
        "Authorization": f'Bearer {bearer_token}'
    }
    search_params = {
        "exclude": "hashtags"
    }

    response = requests.get(base_url, headers=search_headers)
    responce_filtered = requests.get(base_url, headers=search_headers, params=search_params)

    with open('trends.json', 'w') as trends:
        trends.write(json.dumps(response.json(), indent=4))

    with open('trends_filtered.json', 'w') as filter_trends:
        filter_trends.write(json.dumps(responce_filtered.json(), indent=4))
    return response.json(), responce_filtered.json()


if __name__ == '__main__':
    print(get_json())
