import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import *


def get_crypto_value(base_currency="BTC", currency="USD", target_date=None, session=None):
    params = {}
    if target_date is not None:
        params = {'date': target_date}

    url = f"https://api.coinbase.com/v2/prices/{base_currency}-{currency}/spot"

    if session is None:
        response = requests.get(url, params=params).json()
    else:
        response = session.get(url, params=params).json()

    if response.get("errors"):
        raise Exception(response['errors'][0]["message"])
    data = response['data']
    return data['base'], data['currency'], data['amount']


def crypto_graphic(start_date, end_date=datetime.today(), days_interval=30, base_currency="BTC", currency="USD"):
    # 'date_time' is a list of dates in string format.
    date_time = [start_date]

    # 'data' is a list of float that represent the value of the crypto according to the ith date in 'date_time'.
    start_amount = float(get_crypto_value(base_currency, currency, start_date)[-1])
    data = [start_amount]

    date_format = "%Y-%m-%d"

    # while 'new_date' is less than 'end_date' keep adding dates and amounts to 'date_time' and 'data'.
    with requests.Session() as session:
        while True:
            new_date = datetime.strptime(date_time[-1], date_format) + relativedelta(days=days_interval)

            if new_date > end_date:
                end_date_str = end_date.strftime(date_format)
                date_time.append(end_date_str)
                amount = get_crypto_value(base_currency, currency, end_date_str, session)[-1]
                data.append(float(amount))
                break

            new_date_str = new_date.strftime(date_format)
            date_time.append(new_date_str)
            amount = get_crypto_value(base_currency, currency, new_date_str, session)[-1]
            data.append(float(amount))

    # create a data frame with the amounts in the rows and the dates as index. Then plot it.
    date_time = pd.to_datetime(date_time, yearfirst=True)
    DF = pd.DataFrame({"value": data})
    DF = DF.set_index(date_time)
    plt.plot(DF, "y")
    plt.ylabel(f"{base_currency}-{currency}")
    plt.gcf().autofmt_xdate()
    plt.show()



crypto_graphic("2021-02-02", days_interval=30, base_currency="BTC")
# print(get_crypto_value(target_date='2021-05-19'))