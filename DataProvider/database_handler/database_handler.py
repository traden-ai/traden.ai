from DataProvider.database_handler.utils import insert_items, remove_item, query_item, remove_item_metadata, \
    insert_items_metadata, get_item_metadata, get_stocks, get_item, insert_indicators_for_resource_identifier, \
    get_indicators, convert_to_data_by_date, insert_stocks


class DatabaseHandler:

    current_stocks = None

    current_indicators = None

    def insert_data(self, items):
        insert_items(items)
        insert_items_metadata(items)

    def insert_indicators_for_resource_identifier(self, indicators, resource_identifier):
        insert_indicators_for_resource_identifier(indicators, resource_identifier)

    def insert_tickers(self, tickers, type):
        insert_stocks(tickers, type)

    def get_item(self, ticker, date):
        return get_item(ticker, date)

    def get_data_by_stock(self, tickers, indicators, start_date, end_date):
        data = []
        for ticker in tickers:
            data += [query_item(ticker,  indicators, start_date, end_date)]
        return data

    def get_metadata_by_stock_and_indicator(self, stock, indicator):
        return get_item_metadata(stock, indicator)

    def get_data_by_date(self, tickers, indicators, start_date, end_date):
        raw_data = self.get_data_by_stock(tickers, indicators, start_date, end_date)
        return convert_to_data_by_date(raw_data)

    def get_stocks(self, type=None):
        self.current_stocks = get_stocks(type=type)
        return self.current_stocks

    def get_indicators(self, resource_identifier=None):
        self.current_indicators = get_indicators(resource_identifier=resource_identifier)
        return self.current_indicators

    def update_data(self, items):
        insert_items(items)
        insert_items_metadata(items)


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

    def are_indicators_possible(self, received_indicators):
        indicators = get_indicators()
        for indicator in received_indicators:
            if indicator not in indicators:
                return False
        return True

    def are_tickers_possible(self, tickers):
        stocks = get_stocks()
        available_tickers = []
        not_available_tickers = []
        is_possible = True
        for ticker in tickers:
            if ticker not in stocks:
                not_available_tickers.append(ticker)
                is_possible = False
            else:
                available_tickers.append(ticker)
        return is_possible, available_tickers, not_available_tickers

    def is_interval_possible(self, tickers, indicators, start_date, end_date):
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
