import requests

BASE_URL = "https://api.opendota.com/api"
REQUEST_TIMEOUT = (3, 30)


def make_request(url, params=None):
    response = requests.get(
        url,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()
    return response.json()
