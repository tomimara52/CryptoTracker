import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import *
import json
import asyncio
import aiohttp

DATE_FORMAT = "%Y-%m-%d"


def str_to_datetime(str_date: str):
    return datetime.strptime(str_date, DATE_FORMAT)


def datetime_to_str(date_time: datetime):
    return date_time.strftime(DATE_FORMAT)


async def get_crypto_value(session, base_currency="BTC", currency="USD", target_date=None):

    url = f"https://api.coinbase.com/v2/prices/{base_currency}-{currency}/spot"

    if target_date is not None:
        url += '?date=' + target_date

    async with session.get(url) as response:

        data = await response.read()
        json_data = json.loads(data)
        if json_data.get("errors"):
            raise Exception(json_data['errors'][0]["message"])
        data = json_data['data']
        return float(data['amount'])


async def crypto_graphic(start_date, end_date=datetime.today(), days_interval=30, base_currency="BTC", currency="USD"):
    # 'date_time' is a list of dates in string format.
    date_time = [start_date]


    # while 'new_date' is less than 'end_date' keep adding dates and amounts to 'date_time'.

    async with aiohttp.ClientSession() as session:
        tasks = []
        start_amount = asyncio.ensure_future(get_crypto_value(session, base_currency, currency, start_date))
        tasks.append(start_amount)

        while True:
            new_date = str_to_datetime(date_time[-1]) + relativedelta(days=days_interval)

            if new_date > end_date:
                end_date_str = datetime_to_str(end_date)
                date_time.append(end_date_str)
                async_func = asyncio.ensure_future(get_crypto_value(session, base_currency, currency, end_date_str))
                tasks.append(async_func)
                break

            new_date_str = datetime_to_str(new_date)
            date_time.append(new_date_str)
            async_func = asyncio.ensure_future(get_crypto_value(session, base_currency, currency, new_date_str))
            tasks.append(async_func)

        # gather all the amounts returned in 'data' list.
        data = await asyncio.gather(*tasks)


    # create a data frame with the amounts in the rows and the dates as index. Then plot it.
    date_time = pd.to_datetime(date_time, yearfirst=True)
    DF = pd.DataFrame({"value": data})
    DF = DF.set_index(date_time)
    plt.plot(DF, "y")
    plt.ylabel(f"{base_currency}-{currency}")
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    base_currency = input("Which crypto you want to look for? ")
    start_date = input("Since when do you want the data from? (YYYY-MM-DD) ")
    asyncio.run(crypto_graphic(start_date, days_interval=1, base_currency=base_currency))