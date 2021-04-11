from database_handler.handler_calls import get_data
import numpy as np

filepath = "symbols.txt"


def get_stocks(path=filepath):
    """ method that loads all stocks from 'data/symbols.txt' into a list """

    stocks = []
    with open(path, "r") as f:
        for line in f:
            stocks.append(line.strip())

    return stocks


def data_load(stocks: list, start: str, end: str):
    """ method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the database to a numpy array """
    json_data = get_data(stocks)
    return_data = {}
    prices = {}
    for stock_data in json_data:
        return_data[stock_data["Symbol"]] = []
        company_prices = []
        for day in stock_data["Data"]:
            if start <= day <= end:
                return_data[stock_data["Symbol"]].append(stock_data["Data"][day])
                company_prices = [float(stock_data["Data"][day]["CLOSE"])] + company_prices
        prices[stock_data["Symbol"]] = company_prices
    dates = []
    for day in json_data[0]["Data"]:
        if start <= day <= end:
            dates = [day] + dates
    return return_data, dates, prices
