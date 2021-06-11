""" script for grabbing daily data on various stocks and dumping them as individual .json"""

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
from time import sleep

from pandas.core.base import DataError
from pandas.core.frame import DataFrame
from utils.utils import get_stocks, get_indicators
from os import path
import requests
import json
import sys

key = "E9NN094GU5JX53JA"
key_index = 0
keys = ["E9NN094GU5JX53JA",
        "TRWEWUN34X40JD5X",
        "346C7PNCROD4ATR3"
        ]

def get_type_by_indicator(indicator):
    if indicator in ("daily"):
        return get_daily
    elif indicator in ("sma", "ema", "macd", "rsi", "vwap", "cci", "stoch", "adx", "aroon", "bbands", "ad", "obv"):
        return get_tech_indicator
    elif indicator in ("company_overview", "income_statement", "balance_sheet", "cash_flow", "earnings"):
        return get_fundamental_indicator


def get_daily(stock, indicator):
    ts = TimeSeries(key=key, output_format='json')
    if indicator == "daily":
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
    return data


def get_tech_indicator(stock, indicator):
    ts = TechIndicators(key=key, output_format='json')
    if indicator == "sma":
        data, meta_data = ts.get_sma(symbol=stock)
    elif indicator == "ema":
        data, meta_data = ts.get_ema(symbol=stock)
    elif indicator == "macd":
        data, meta_data = ts.get_macd(symbol=stock)
    elif indicator == "rsi":
        data, meta_data = ts.get_rsi(symbol=stock)
    elif indicator == "vwap":
        data, meta_data = ts.get_vwap(symbol=stock)
    elif indicator == "cci":
        data, meta_data = ts.get_cci(symbol=stock)
    elif indicator == "stoch":
        data, meta_data = ts.get_stoch(symbol=stock)
    elif indicator == "adx":
        data, meta_data = ts.get_adx(symbol=stock)
    elif indicator == "aroon":
        data, meta_data = ts.get_aroon(symbol=stock)
    elif indicator == "bbands":
        data, meta_data = ts.get_bbands(symbol=stock)
    elif indicator == "ad":
        data, meta_data = ts.get_ad(symbol=stock)
    elif indicator == "obv":
        data, meta_data = ts.get_obv(symbol=stock)

    return data



def get_fundamental_indicator(stock, indicator):
    ts = FundamentalData(key=key, output_format='json')
    if indicator == "company_overview":
        data, meta_data = ts.get_company_overview(symbol=stock)
    elif indicator == "earnings":
        url = "https://www.alphavantage.co/query?function=EARNINGS&symbol={}&apikey={}".format(stock, key)
        raw = requests.get(url)
        data = raw.json()
    elif indicator == "cash_flow":
        data, meta_data = ts.get_cash_flow_quarterly(symbol=stock)
    elif indicator == "income_statement":
        data, meta_data = ts.get_income_statement_quarterly(symbol=stock)
    elif indicator == "balance_sheet":
        data, meta_data = ts.get_balance_sheet_quarterly(symbol=stock)
    return data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    stocks = get_stocks()
    index = 0
    stock_index = 0
    indicator_index = 0
    indicators = get_indicators()
    size = len(stocks) * len(indicators)

    while index != size:
        try:
            ticker = stocks[stock_index]
            indicator = indicators[indicator_index]
            if not path.exists("alpha_vantage/{}_{}.json".format(ticker, indicator)):
                data = get_type_by_indicator(indicator)(ticker, indicator)

                if ("Note" in data.keys()):
                    # alpha vantage returns limit without raising exception
                    raise Exception

                with open("alpha_vantage/{}_{}.json".format(ticker, indicator), 'x') as f:
                    if type(data) == DataFrame:
                        json.dump(data.to_json(orient="index"), f)
                    else:
                        json.dump(data, f)
            if indicator_index == len(indicators) - 1:
                stock_index += 1
            index += 1
            indicator_index = (indicator_index + 1) % len(indicators)

            print("success on {} with key {}".format(ticker, key))
        except Exception as e:
            key_index = (key_index+1) % len(keys)
            key = keys[key_index]
            print("exception on {} with key {}\n{}".format(ticker, key, e))    
