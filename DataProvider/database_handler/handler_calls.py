from DataProvider.database_handler.utils import insert_items, remove_item, query_item


def insert_data(items):
    insert_items(items)


def get_item(ticker, date):
    return get_item(ticker, date)


def get_data(tickers, start_date, end_date):
    data = []
    for ticker in tickers:
        data += [query_item(ticker, start_date, end_date)]
    return data


def update_data(items):
    for item in items:
        insert_items(item)


def delete_data(tickers):
    for ticker in tickers:
        remove_item(ticker)
