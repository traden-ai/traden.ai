""" script for grabbing daily data on various stocks and dumping them as individual .json"""

from alpha_vantage.timeseries import TimeSeries
from time import sleep
import json


def get_stocks():
    ''' method that loads all stocks from 'symbols.txt' into a list '''

    stocks = []
    with open("symbols.txt", "r") as f:
        for line in f:
            stocks.append(line.strip())

    return stocks

def get_daily(stock):
    # use your alpha_vantage api key
    ts = TimeSeries(key='', output_format='json')
    data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
    return data


if __name__ == "__main__":
    stocks = get_stocks()
    size = len(stocks)
    index = 0

    while index != size:
        try:
            ticker = stocks[index]
            daily = get_daily(ticker)
            with open("{}.json".format(ticker), 'w') as f:
                json.dump(daily, f)

            index += 1

            print("success on {}".format(ticker))
        except Exception as e:
            print("exception on {}, sleeping\n{}".format(ticker, e))    
            sleep(60)