import json
from database_handler.handler_calls import insert_data, query_item, remove_item
from utils.utils import get_stocks


def convert_ticker_files_into_data(ticker, indicators):
    mainDict = None
    for indicator in indicators:
        with open("alpha_vantage/{}_{}.json".format(ticker, indicator)) as f:
            if not mainDict:
                mainDict = json.load(f)
            else:
                data = json.load(f)
                for key in data:
                    if key not in mainDict:
                        continue
                    mainDict[key].update(data[key])
    return delete_entries_with_non_maximum_len(mainDict)


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
                                                ["daily", "sma", "ema", "macd", "rsi", "cci", "adx", "stoch"])
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

