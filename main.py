import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import *


def get_crypto_value(base_currency="BTC", currency="USD", target_date=None):
    params = {}
    if target_date is not None:
        params = {'date': target_date}

    url = f"https://api.coinbase.com/v2/prices/{base_currency}-{currency}/spot"
    response = requests.get(url, params=params).json()
    if response.get("errors"):
        raise Exception(response['errors'][0]["message"])
    data = response['data']
    return data['base'], data['currency'], data['amount']


def crypto_graphic(start_date, end_date=datetime.today(), days_interval=30, base_currency="BTC", currency="USD"):
    date_time = [start_date]
    start_amount = float(get_crypto_value(base_currency, currency, start_date)[-1])
    data = [start_amount]
    date_format = "%Y-%m-%d"

    while True:
        new_date = datetime.strptime(date_time[-1], date_format) + relativedelta(days=days_interval)

        if new_date > end_date:
            end_date_str = end_date.strftime(date_format)
            date_time.append(end_date_str)
            amount = get_crypto_value(base_currency, currency, end_date_str)[-1]
            data.append(float(amount))
            break

        new_date_str = new_date.strftime(date_format)
        date_time.append(new_date_str)
        amount = get_crypto_value(base_currency, currency, new_date_str)[-1]
        data.append(float(amount))

    date_time = pd.to_datetime(date_time, yearfirst=True)
    # for date_ in date_time:
    #     amount = get_crypto_value(base_currency, currency, date_)[-1]
    #     data.append(float(amount))

    DF = pd.DataFrame({"value": data})
    DF = DF.set_index(date_time)
    plt.plot(DF, "y")
    plt.ylabel(f"{base_currency}-{currency}")
    plt.gcf().autofmt_xdate()
    plt.show()



crypto_graphic("2021-02-02", days_interval=30, base_currency="BTC")
# print(get_crypto_value(target_date='2021-05-19'))