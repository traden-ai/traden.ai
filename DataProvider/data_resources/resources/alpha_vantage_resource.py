import json

import requests
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from retrying import retry

from DataProvider.data_resources.data_resource_interface import DataResourceInterface
from DataProvider.data_resources.resources.utils import *


class AlphaVantage(DataResourceInterface):
    name = "AlphaVantage"

    description = "API for stock indicators"

    def __init__(self, key="E9NN094GU5JX53JA"):
        self.key = key

    def get_description(self):
        return self.description

    def get_daily_data(self, tickers: list, indicators: list) -> list:
        """Data Resource should return respective data in the format
        {indicator: data in string format}
        """
        pass

    def get_past_data(self, tickers: list, indicators: list, start_date: str, end_date: str):
        """Data Resource should return past data in the format
        {ticker : {date: {indicator: data in string format, ...}, ...}, ...}
        """
        past_data = {}
        for ticker in tickers:
            if ticker not in past_data:
                past_data[ticker] = {}
            for indicator in indicators:
                data, meta_data = self.get_type_by_indicator(indicator)(ticker, indicator)
                filtered_data = self.filter_using_dates(data, start_date, end_date)
                for date in filtered_data:
                    if date in past_data[ticker]:
                        past_data[ticker][date].update({indicator: filtered_data[date]})
                    else:
                        past_data[ticker][date] = {indicator: filtered_data[date]}
        return past_data

    def get_type_by_indicator(self, indicator):
        if indicator in ("dailyAdjusted",):
            return self.get_daily
        elif indicator in ("sma", "ema", "macd", "rsi", "vwap", "cci", "stoch", "adx", "aroon", "bbands", "ad", "obv"):
            return self.get_tech_indicator
        elif indicator in ("companyOverview", "incomeStatement", "balanceSheet", "cashFlow", "earnings"):
            return self.get_fundamental_indicator

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=120000)
    def get_daily(self, stock, indicator):
        ts = TimeSeries(key=self.key, output_format='json')
        data, meta_data = None, None
        if indicator == "dailyAdjusted":
            data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')
            data = transform_key_to(data, dailyAdjustedOld2NewNames)
        return data, meta_data

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=240000)
    def get_tech_indicator(self, stock, indicator):
        ts = TechIndicators(key=self.key, output_format='json')
        data, meta_data = None, None
        if indicator == "sma":
            data20, meta_data = ts.get_sma(symbol=stock, time_period=20)
            data20 = transform_key_to(data20, {"SMA": "sma20"})
            data50, meta_data = ts.get_sma(symbol=stock, time_period=50)
            data50 = transform_key_to(data50, {"SMA": "sma50"})
            data100, meta_data = ts.get_sma(symbol=stock, time_period=100)
            data100 = transform_key_to(data100, {"SMA": "sma100"})
            data = unite_data(unite_data(data100, data50), data20)
        elif indicator == "ema":
            data20, meta_data = ts.get_ema(symbol=stock, time_period=20)
            data20 = transform_key_to(data20, {"EMA": "ema20"})
            data50, meta_data = ts.get_ema(symbol=stock, time_period=50)
            data50 = transform_key_to(data50, {"EMA": "ema50"})
            data100, meta_data = ts.get_ema(symbol=stock, time_period=100)
            data100 = transform_key_to(data100, {"EMA": "ema100"})
            data = unite_data(unite_data(data100, data50), data20)
        elif indicator == "macd":
            data, meta_data = ts.get_macd(symbol=stock)
            data = transform_key_to(data, macdOld2NewNames)
        elif indicator == "rsi":
            data, meta_data = ts.get_rsi(symbol=stock)
            data = transform_key_to(data, rsiOld2NewNames)
        elif indicator == "vwap":
            data, meta_data = ts.get_vwap(symbol=stock)
            data = transform_key_to(data, vwapOld2NewNames)
        elif indicator == "cci":
            data, meta_data = ts.get_cci(symbol=stock)
            data = transform_key_to(data, cciOld2NewNames)
        elif indicator == "stoch":
            data, meta_data = ts.get_stoch(symbol=stock)
            data = transform_key_to(data, stochOld2NewNames)
        elif indicator == "adx":
            data, meta_data = ts.get_adx(symbol=stock)
            data = transform_key_to(data, adxOld2NewNames)
        elif indicator == "aroon":
            data, meta_data = ts.get_aroon(symbol=stock)
            data = transform_key_to(data, aroonOld2NewNames)
        elif indicator == "bbands":
            data, meta_data = ts.get_bbands(symbol=stock)
            data = transform_key_to(data, bbandsOld2NewNames)
        elif indicator == "ad":
            data, meta_data = ts.get_ad(symbol=stock)
            data = transform_key_to(data, adOld2NewNames)
        elif indicator == "obv":
            data, meta_data = ts.get_obv(symbol=stock)
            data = transform_key_to(data, obvOld2NewNames)

        return data, meta_data

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=240000)
    def get_fundamental_indicator(self, stock, indicator):
        ts = FundamentalData(key=self.key, output_format='json')
        data, meta_data = None, None
        if indicator == "companyOverview":
            data, meta_data = ts.get_company_overview(symbol=stock)
            # TODO delete Description
            data = transform_key_to(data, companyOverviewOld2NewNames)
        elif indicator == "earnings":
            url = "https://www.alphavantage.co/query?function=EARNINGS&symbol={}&apikey={}".format(stock, self.key)
            raw = requests.get(url)
            data = raw.json()["quarterlyEarnings"]
            processed_data = {}
            for it in data:
                processed_data[it["fiscalDateEnding"]] = it
            data = transform_key_to(processed_data, earningsOld2NewNames)
        elif indicator == "cashFlow":
            data, meta_data = ts.get_cash_flow_quarterly(symbol=stock)
            data = json.loads(data.to_json(orient="index"))
            processed_data = {}
            for it in data:
                processed_data[data[it]["fiscalDateEnding"]] = data[it]
            data = processed_data
        elif indicator == "incomeStatement":
            data, meta_data = ts.get_income_statement_quarterly(symbol=stock)
            data = json.loads(data.to_json(orient="index"))
            processed_data = {}
            for it in data:
                processed_data[data[it]["fiscalDateEnding"]] = data[it]
            data = transform_key_to(processed_data, incomeStatementOld2NewNames)
        elif indicator == "balanceSheet":
            data, meta_data = ts.get_balance_sheet_quarterly(symbol=stock)
            data = json.loads(data.to_json(orient="index"))
            processed_data = {}
            for it in data:
                processed_data[data[it]["fiscalDateEnding"]] = data[it]
            data = transform_key_to(processed_data, balanceSheetOld2NewNames)
        return data, meta_data

    def filter_using_dates(self, data, start_date, end_date):
        filtered_date = {}
        for date in data:
            if start_date <= date <= end_date:
                filtered_date[date] = data[date]
        return filtered_date

if __name__ == "__main__":
    av = AlphaVantage()
    data = av.get_past_data(["A"], ["balanceSheet"], "2020-01-01", "2021-01-01")
    print(data)