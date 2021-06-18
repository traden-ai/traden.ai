from DataProvider.database_handler.utils import insert_items, remove_item, query_item, remove_item_metadata, \
    insert_items_metadata, get_item_metadata, get_stocks, get_item, insert_indicators_for_resource_identifier, \
    get_indicators


class DatabaseHandler:

    def insert_data(self, items):
        insert_items(items)
        insert_items_metadata(items)

    def insert_indicators_for_resource_identifier(self, indicators, resource_identifier):
        insert_indicators_for_resource_identifier(indicators, resource_identifier)

    def get_item(self, ticker, date):
        return get_item(ticker, date)

    def get_data(self, tickers, start_date, end_date):
        data = []
        for ticker in tickers:
            data += [query_item(ticker, start_date, end_date)]
        return data

    def get_stocks(self):
        return get_stocks()

    def get_indicators(self, resource_identifier=None):
        return get_indicators(resource_identifier=None)

    def update_data(self, items):
        for item in items:
            insert_items(item)

    def update_item(self, ticker, date, indicator, value):
        item = get_item(ticker, date)
        if date in item:
            item[date][indicator] = value
        else:
            item[date] = {}
            item[date][indicator] = value
        insert_items([item])
        insert_items_metadata([item])

    def delete_data(self, tickers):
        for ticker in tickers:
            remove_item(ticker)
            remove_item_metadata(ticker)


def is_interval_possible(tickers, indicators, start_date, end_date):
    possible_start_date = None
    possible_end_date = None
    for ticker in tickers:
        for indicator in indicators:
            metadata = get_item_metadata(ticker, indicator)
            if not possible_start_date:
                possible_start_date = metadata["StartDate"]
            if not possible_end_date:
                possible_end_date = metadata["EndDate"]
            if possible_start_date < metadata["StartDate"]:
                possible_start_date = metadata["StartDate"]
            if possible_end_date > metadata["EndDate"]:
                possible_end_date = metadata["EndDate"]
    return start_date > possible_start_date and end_date < possible_end_date, possible_start_date, possible_end_date
