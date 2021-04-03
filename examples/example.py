import requests


def get_json():
    """
    Function sent request to Twitter Api and  get .json object with information about current twitter user.
    """
    base_url = "https://api.twitter.com/1.1/trends/place.json?id=1"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAKkSNAEAAAAADGjajQeyVyQTi28qCAff1Mrl520%3DGzjvYM2YJgXGIMZQzXE23E4jUcSmIsOpsGCQcAnhL87so6O4JC"

    search_headers = {
        "Authorization": f'Bearer {bearer_token}'
    }

    response = requests.get(base_url, headers=search_headers)
    return response.json()


if __name__ == '__main__':
    print(get_json())
