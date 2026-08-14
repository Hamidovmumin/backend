import requests
from django.core.cache import cache

URLS = [
    "https://api.frankfurter.dev/v2/rate/EUR/AZN",
    "https://api.frankfurter.dev/v2/rate/USD/AZN",
]

def fetch_currency_rates() ->None:
    print('Fetching currency rates...')

    for url in URLS:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate_value = data["rate"]
            rate_currency = data["base"]

            cache.set(f'currency_rate:{rate_currency}', rate_value, timeout=None)

        except requests.RequestException as e:
            print(e)