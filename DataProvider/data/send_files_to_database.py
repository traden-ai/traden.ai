import json
from database_handler.handler_calls import insert_data, query_item, remove_item
from utils.utils import get_stocks, get_indicators
from datetime import date as dt
from dateutil.relativedelta import relativedelta

def convert_ticker_files_into_data(ticker, indicators):
    mainDict = {}
    fiscalDict = {}
    for indicator in indicators:
        with open("alpha_vantage/{}_{}.json".format(ticker, indicator)) as f:
            data = json.load(f)
            if indicator not in ("cash_flow", "balance_sheet", "income_statement", "earnings"):
                for key in data:
                    if key not in mainDict:
                        mainDict[key] = {}
                        mainDict[key][indicator] = data[key]
                    else:
                        mainDict[key][indicator] = data[key]
            else:
                if indicator == "earnings":
                    for dict in data["quarterlyEarnings"]:
                        fiscal_date = dict["fiscalDateEnding"]
                        if fiscal_date not in fiscalDict:
                            fiscalDict[fiscal_date] = {}
                            fiscalDict[fiscal_date][indicator] = dict
                        fiscalDict[fiscal_date][indicator] = dict
                else:
                    data = json.loads(data)
                    for key in data:
                        fiscal_date = data[key]["fiscalDateEnding"]
                        if fiscal_date not in fiscalDict:
                            fiscalDict[fiscal_date] = {}
                            fiscalDict[fiscal_date][indicator] = data[key]
                        fiscalDict[fiscal_date][indicator] = data[key]
    mainDict = delete_entries_with_non_maximum_len(mainDict)
    for fiscal_date in fiscalDict:
        for date in mainDict:
            parts = fiscal_date.split("-")
            date_parts = date.split("-")
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
            date_date_time = dt(year, month, day)
            fiscal_year, fiscal_month, fiscal_day = int(parts[0]), int(parts[1]), int(parts[2])
            fiscal_date_time = dt(fiscal_year, fiscal_month, fiscal_day)
            next_fiscal_date_time = fiscal_date_time + relativedelta(months=+3)
            if next_fiscal_date_time > date_date_time >= fiscal_date_time:
                for indicator in fiscalDict[fiscal_date]:
                    mainDict[date][indicator] = fiscalDict[fiscal_date][indicator]
    return mainDict


def delete_entries_with_non_maximum_len(dict):
    max = find_max_entry_size(dict)
    new_dict = {}
    for key in dict:
        if len(dict[key]) == max:
            new_dict[key] = dict[key]
    return new_dict


def find_max_entry_size(dict):
    max = 0
    for key in dict:
        if len(dict[key]) > max:
            max = len(dict[key])
    return max


def transform_name(dict, current_name, new_name):
    new_dict = {}
    for date in dict:
        new_date_dict = {}
        for key in dict[date]:
            if key == current_name:
                new_date_dict[new_name] = dict[date][key]
            else:
                new_date_dict[key] = dict[date][key]
        new_dict[date] = new_date_dict
    return new_dict


def return_specified_format(ticker, data):
    return {"Symbol": ticker, "Data": data}

def save_stock(i):
    print("Currently in stock {}, with index {}".format(tickers[i], i))
    stock_data = convert_ticker_files_into_data(tickers[i],
                                                get_indicators())
    insert_data([return_specified_format(tickers[i], stock_data)])


#TODO solve add metric use case

if __name__ == '__main__':
    import sys
    import concurrent.futures
    lst = []
    tickers = get_stocks()
    start = 0
    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(save_stock, i) for i in range(start, len(tickers))]
    concurrent.futures.wait(futures)