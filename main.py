import requests
import matplotlib.pyplot as plt
from datetime import date


def get_crypto_value(base_currency="BTC", currency="USD", target_date=None):
    params = {}
    if target_date is not None:
        params = {'date': target_date}

    url = f"https://api.coinbase.com/v2/prices/{base_currency}-{currency}/spot"
    response = requests.get(url, params=params).json()
    return response


def print_crypto_value(json):
    if json.get('errors'):
        print(json['errors'][0]['message'])
        return

    data = json["data"]
    print(f"{data['base']}-{data['currency']}:{data['amount']}")


def crypto_graphic(start_date, end_date=date.today(), months_interval=1, base_currency="BTC", currency="USD"):
    pass



# print_crypto_value(get_crypto_value(target_date="2020-02-02"))
plt.plot([1, 2, 3, 4],[10,20,30,40,50])
plt.ylabel('some numbers')
plt.show()