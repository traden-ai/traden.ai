from .utils import insert_items, remove_multiple, remove_item, query_item, get_entire_collection, update_item


def insert_data(items):
    insert_items(items)


def get_all_data():
    return get_entire_collection()


def get_data(tickers):
    data = []
    for ticker in tickers:
        data += [query_item(ticker)]
    return data


def update_data(items):
    for item in items:
        update_item(item["Symbol"], item["Data"])


def delete_all_data():
    remove_multiple({})


def delete_data(tickers):
    for ticker in tickers:
        remove_item(ticker)
