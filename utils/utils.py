import datetime as dt

import numpy as np
from Models.models.action import Action
from Simulation.simulation_data.simulation_data import SimulationData

symbols_filepath = "../data/symbols.txt"
keys_filepath = "../data/keys.txt"
indicators_filepath = "../data/indicators.txt"
proxies_filepath = "../data/proxies.txt"


def profit_percentage_by_year(initial_value, current_value, time_in_days):
    return (((((current_value - initial_value) / initial_value) + 1) ** (365 / time_in_days)) - 1) * 100


def time_between_days(start_date, end_date):
    from datetime import date
    year0, month0, day0 = get_year_month_day(start_date)
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


def convert_daily_data_to_np(daily_data):
    result = {}
    vec = []
    attributes = None
    for s in daily_data:
        if not attributes:
            attributes = [a for a in dir(daily_data[s]) if not a.startswith('__') and not callable(getattr(daily_data[s], a))]
            attributes = sorted(attributes)
        for attr in attributes:
            attr_dict = getattr(daily_data[s], attr)
            keys = sorted(list(attr_dict))
            attribute_components_values = [attr_dict[key] for key in keys]
            if attribute_components_values != []:
                vec.extend(attribute_components_values)
        result[s] = np.array(vec)
        vec = []
    return result


def convert_data_to_np(data_raw):
    matrix = {}
    stock_matrix = {}
    for day in data_raw:
        for stock in data_raw[day]:
            daily_np = convert_daily_data_to_np({stock: SimulationData(**data_raw[day][stock])})
            if stock not in stock_matrix:
                stock_matrix[stock] = []
            stock_matrix[stock].append(daily_np[stock])
    for stock in stock_matrix:
        matrix[stock] = np.stack(stock_matrix[stock], axis=-1)
    return matrix


def convert_prices_to_np(prices_raw):
    price_matrix = {}
    elements = {}
    for day in prices_raw:
        for stock in day:
            if stock not in elements:
                elements[stock] = []
            elements[stock].append(day[stock])
    for stock in elements:
        price_matrix[stock] = np.array(elements[stock]).reshape(-1, 1)
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

"""
def data_load(stocks: list, start: str, end: str):
    method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the database to a numpy array
    json_data = get_data(stocks, start, end)
    return_data = {}
    prices = {}
    for stock_data in json_data:
        return_data[stock_data["Symbol"]] = []
        company_prices = []
        for day in stock_data["Data"]:
            if start <= day <= end and all(day in sd["Data"] for sd in json_data):
                return_data[stock_data["Symbol"]].append(stock_data["Data"][day])
                company_prices.append(float(stock_data["Data"][day]["daily"]["4. close"]))
        prices[stock_data["Symbol"]] = company_prices
    dates = []
    for day in json_data[0]["Data"]:
        if start <= day <= end and all(day in sd["Data"] for sd in json_data):
            dates.append(day)
    return dates, return_data, prices"""


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
            if action["Ticker"] not in final_dict:
                final_dict[action["Ticker"]] = []
            final_dict[action["Ticker"]].append(action)
    return final_dict


def majority_voting(actions):
    actions_dict = filter_by_ticket(actions)
    final_actions = []
    for s in actions_dict:
        no_buys = 0
        buy_intensity_sum = 0
        no_sells = 0
        sell_intensity_sum = 0
        for action in actions_dict[s]:
            if action["Action"] == Action.SELL:
                sell_intensity_sum += action["Intensity"]
                no_sells += 1
            elif action["Action"] == Action.BUY:
                buy_intensity_sum += action["Intensity"]
                no_buys += 1
        if no_buys > len(actions_dict[s]) / 2:
            final_actions.append({"Ticker": s, "Action": Action.BUY, "Intensity": buy_intensity_sum / no_buys})
        elif no_sells > len(actions_dict[s]) / 2:
            final_actions.append({"Ticker": s, "Action": Action.SELL, "Intensity": sell_intensity_sum / no_sells})
    return final_actions


def convert_nominal_to_variation_2D(np_arr_raw, eps=0.001):
    np_arr = np_arr_raw.transpose()
    new_arr = []
    for i in range(1, len(np_arr)):
        features = []
        for j in range(len(np_arr[i])):
            if np_arr[i - 1][j] != 0:
                features.append(np_arr[i][j] / np_arr[i - 1][j])
            else:
                features.append(np_arr[i][j] / eps)
        new_arr.append(features)
    return np.array(new_arr).transpose()


def convert_nominal_to_variation_1D(np_arr, eps=0.001):
    new_arr = []
    for i in range(1, len(np_arr)):
        if np_arr[i - 1] != 0:
            new_arr.append(np_arr[i] / np_arr[i - 1])
        else:
            new_arr.append(np_arr[i] / eps)
    return np.array(new_arr)
