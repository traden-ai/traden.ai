import datetime as dt

import numpy as np
from database_handler.handler_calls import get_data

symbols_filepath = "../data/symbols.txt"
keys_filepath = "../data/keys.txt"
indicators_filepath = "../data/indicators.txt"
proxies_filepath = "../data/proxies.txt"


def profit_percentage_by_year(initial_value, current_value, time_in_days):
    return (((((current_value - initial_value) / initial_value) + 1) ** (365 / time_in_days)) - 1) * 100


def time_between_days(initial_date, end_date):
    from datetime import date
    year0, month0, day0 = get_year_month_day(initial_date)
    year1, month1, day1 = get_year_month_day(end_date)
    d0 = date(int(year0), int(month0), int(day0))
    d1 = date(int(year1), int(month1), int(day1))
    delta = d1 - d0
    return delta.days


def get_year_month_day(date):
    date_parts = date.split("-")
    year = date_parts[0]
    month = date_parts[1]
    day = date_parts[2]
    return year, month, day


def get_year(date):
    date_parts = date.split("-")
    year = date_parts[0]
    return year


def get_month(date):
    date_parts = date.split("-")
    month = date_parts[1]
    return month


def date_smaller_or_equal(date1: str, date2: str):
    date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
    date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
    return date1_datetime <= date2_datetime


def date_bigger_or_equal(date1: str, date2: str):
    date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
    date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
    return date1_datetime >= date2_datetime


def get_date_index(data_year: list, date: str, date_type: str):
    for index, data_day in enumerate(data_year):
        if date_bigger_or_equal(data_day["date"], date) and date_type == "start" or \
                not date_smaller_or_equal(data_day["date"], date) and date_type == "end":
            break

    return index


def convert_daily_data_to_np(daily_data: dict, keys=
(
        "4. close", "1. open", "2. high", "3. low", "5. volume", "SMA", "EMA", "MACD_Hist", "MACD_Signal", "MACD",
        "CCI", "RSI",
        "ADX", "SlowD", "SlowK")):
    result = {}
    matrix = []

    for s in daily_data:
        vec = [daily_data[s][el] for el in keys]
        result[s] = np.array(vec)
    return result


def convert_data_to_np(data_raw):
    matrix = {}
    stock_matrix = []

    for stock in data_raw:
        for index in range(len(data_raw[stock])):
            stock_matrix.append([convert_daily_data_to_np({stock: data_raw[stock][index]})[stock]])
        matrix[stock] = np.concatenate(stock_matrix, axis=0)
        stock_matrix = []
    return matrix


def convert_prices_to_np(prices_raw):
    price_matrix = {}

    for stock in prices_raw:
        elements = [price for price in prices_raw[stock]]
        price_matrix[stock] = np.array(elements).reshape(-1, 1)
    return price_matrix


def get_proxies(path=proxies_filepath):
    proxies = []
    with open(path, "r") as f:
        for line in f:
            proxies.append(line.strip())

    return proxies


def get_stocks(path=symbols_filepath):
    stocks = []
    with open(path, "r") as f:
        for line in f:
            stocks.append(line.strip())

    return stocks


def get_keys(path=keys_filepath):
    keys = []
    with open(path, "r") as f:
        for line in f:
            keys.append(line.strip())
    return keys


def get_indicators(path=indicators_filepath):
    indicators = []
    with open(path, "r") as f:
        for line in f:
            indicators.append(line.strip())
    return indicators


def data_load(stocks: list, start: str, end: str):
    """ method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the database to a numpy array """
    json_data = get_data(stocks, start, end)
    return_data = {}
    prices = {}
    for stock_data in json_data:
        return_data[stock_data["Symbol"]] = []
        company_prices = []
        for day in stock_data["Data"]:
            if start <= day <= end:
                return_data[stock_data["Symbol"]].append(stock_data["Data"][day])
                company_prices.append(float(stock_data["Data"][day]["daily"]["4. close"]))
        prices[stock_data["Symbol"]] = company_prices
    dates = []
    for day in json_data[0]["Data"]:
        if start <= day <= end:
            dates.append(day)
    return return_data, dates, prices


def vector_proj_of_vec1_on_vec2(vec1: list, vec2: list):
    u = np.array(vec1)
    v = np.array(vec2)

    v_norm = np.sqrt(sum(v ** 2))

    proj_of_u_on_v = (np.dot(u, v) / v_norm ** 2) * v
    return proj_of_u_on_v


def convert_dict_if_equal_keys_to_array(dict1: dict, dict2: dict):
    if dict1.keys() == dict2.keys():
        array1 = []
        array2 = []
        for key in dict1.keys():
            array1.append(dict1[key])
            array2.append(dict2[key])
        return array1, array2


def filter_by_ticket(actions: list):
    final_dict = {}
    for model_actions in actions:
        for action in model_actions:
            if model_actions[action]["Ticker"] not in final_dict:
                final_dict[model_actions[action]["Ticker"]] = []
            final_dict[model_actions[action]["Ticker"]].append(model_actions[action])
    return final_dict
