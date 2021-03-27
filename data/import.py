""" script for grabbing daily data on various stocks and dumping them as individual .json"""

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from time import sleep
from os import path
import json


def get_stocks():
    """ method that loads all stocks from 'symbols.txt' into a list """
    stocks = []
    with open("symbols.txt", "r") as f:
        for line in f:
            stocks.append(line.strip())
    return stocks


def get_daily(stock):
    # use your alpha_vantage api key
    ts = TimeSeries(key="E9NN094GU5JX53JA", output_format='json')
    data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
    return data


def get_tech_indicator(stock, indicator):
    ts = TechIndicators(key="E9NN094GU5JX53JA", output_format='json')
    if indicator == "sma":
        data, meta_data = ts.get_sma(symbol=stock)
    elif indicator == "ema":
        data, meta_data = ts.get_ema(symbol=stock)
    elif indicator == "macd":
        data, meta_data = ts.get_macd(symbol=stock)
    elif indicator == "rsi":
        data, meta_data = ts.get_rsi(symbol=stock)
    return data


if __name__ == "__main__":
    stocks = get_stocks()
    size = len(stocks)
    index = 0

    while index != size:
        try:
            ticker = stocks[index]
            if not path.exists("{}.json".format(ticker)):
                daily = get_tech_indicator(ticker, "rsi")
                with open("{}_rsi.json".format(ticker), 'w') as f:
                    json.dump(daily, f)
            index += 1

            print("success on {}".format(ticker))
        except Exception as e:
            print("exception on {}, trying different key\n{}".format(ticker, e))
            sleep(60)
