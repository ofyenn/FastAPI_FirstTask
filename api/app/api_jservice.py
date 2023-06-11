import requests


def get_date(num):
    try:
        response = requests.get(
            "https://jservice.io/api/random?count=" + str(num)
        )
        if response.status_code == 200:
            result = response.json()
            return result
    except requests.exceptions.RequestException:
        pass

    return ""