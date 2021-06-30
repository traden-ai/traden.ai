import json

import requests
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from retrying import retry

from DataProvider.data_resources.data_resource_interface import DataResourceInterface
from DataProvider.data_resources.resources.utils import retry_if_value_error, transform_key_to


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
                        past_data[ticker][date].update({indicator: json.dumps(filtered_data[date])})
                    else:
                        past_data[ticker][date] = {indicator: json.dumps(filtered_data[date])}
        return past_data

    def get_type_by_indicator(self, indicator):
        if indicator in ("daily"):
            return self.get_daily
        elif indicator in ("sma", "ema", "macd", "rsi", "vwap", "cci", "stoch", "adx", "aroon", "bbands", "ad", "obv"):
            return self.get_tech_indicator
        elif indicator in ("company_overview", "income_statement", "balance_sheet", "cash_flow", "earnings"):
            return self.get_fundamental_indicator

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=30000)
    def get_daily(self, stock, indicator):
        ts = TimeSeries(key=self.key, output_format='json')
        data, meta_data = None, None
        if indicator == "daily":
            data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        return data, meta_data

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=30000)
    def get_tech_indicator(self, stock, indicator):
        ts = TechIndicators(key=self.key, output_format='json')
        data, meta_data = None, None
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

        return data, meta_data

    @retry(retry_on_exception=retry_if_value_error, wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_delay=30000)
    def get_fundamental_indicator(self, stock, indicator):  # TODO fix fundamental data to return data correctly
        ts = FundamentalData(key=self.key, output_format='json')
        data, meta_data = None, None
        if indicator == "company_overview":
            data, meta_data = ts.get_company_overview(symbol=stock)
        elif indicator == "earnings":
            url = "https://www.alphavantage.co/query?function=EARNINGS&symbol={}&apikey={}".format(stock, self.key)
            raw = requests.get(url)
            data = raw.json()
            print(data)
        elif indicator == "cash_flow":
            data, meta_data = ts.get_cash_flow_quarterly(symbol=stock)
        elif indicator == "income_statement":
            data, meta_data = ts.get_income_statement_quarterly(symbol=stock)
            data = data.to_json(orient="index")
        elif indicator == "balance_sheet":
            data, meta_data = ts.get_balance_sheet_quarterly(symbol=stock)
        return data, meta_data

    def filter_using_dates(self, data, start_date, end_date):
        filtered_date = {}
        for date in data:
            if start_date <= date <= end_date:
                filtered_date[date] = data[date]
        return filtered_date

if __name__=="__main__":
    av = AlphaVantage()
    av.get_past_data(["GM"], ["sma", "macd"], "2020-01-01","2021-01-01")