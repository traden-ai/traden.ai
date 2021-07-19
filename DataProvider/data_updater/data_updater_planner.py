import concurrent.futures

from DataProvider.data_updater.utils import chunks
from DataProvider.data_updater.constants import MAXIMUM_DATE
from DataProvider.database_handler.database_handler import DatabaseHandler


class DataUpdaterPlanner:

    def __init__(self, database_handler, id=1):
        self.id = id
        self.database_handler = database_handler

    def update_task_list(self, update_date, workers=10):
        stocks = self.database_handler.get_stocks()
        indicators = self.database_handler.get_indicators()
        futures = []
        executor = concurrent.futures.ProcessPoolExecutor(workers)
        for stock in stocks:
            futures.append(executor.submit(self.update_ticker_tasks, stock, indicators, update_date))
        concurrent.futures.wait(futures)

    def update_ticker_tasks(self, stock, indicators, update_date):
        tasks = []
        for indicator in indicators:
            metadata = self.database_handler.get_metadata_by_stock_and_indicator(stock, indicator)
            if metadata["EndDate"] is None or metadata["StartDate"] is None:
                tasks.append({"Ticker": stock,
                              "Indicator": indicator,
                              "StartDate": None})
            elif update_date > metadata["EndDate"]:
                tasks.append({"Ticker": stock,
                              "Indicator": indicator,
                              "StartDate": metadata["EndDate"]})
        print("Planned tasks for {}".format(stock))
        self.database_handler.insert_tasks(tasks)

