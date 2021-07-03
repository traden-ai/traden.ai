from DataProvider.data_updater.utils import chunks


class DataUpdaterPlanner:

    def __init__(self, database_handler, id=1):
        self.id = id
        self.database_handler = database_handler

    def get_tasks(self, update_date, chunk_size=1, worker=1):
        """returns a list of future actions, the list should have the following format
        [action_item1, action_item2, action_item3, ...]"""
        task_no = self.id + worker
        stocks = self.database_handler.get_stocks()
        indicators = self.database_handler.get_indicators()
        tasks = []
        for stock in stocks:
            for indicator in indicators:
                metadata = self.database_handler.get_metadata_by_stock_and_indicator(stock, indicator)
                if metadata["EndDate"] is None or metadata["StartDate"] is None:
                    tasks.append({"Ticker": stock,
                                  "Indicator": indicator,
                                  "StartDate": None,
                                  "EndDate": None})
                elif update_date > metadata["EndDate"]: #TODO probably also necessary to check if update was done recently
                    tasks.append({"Ticker": stock,
                                  "Indicator": indicator,
                                  "StartDate": metadata["EndDate"],
                                  "EndDate": update_date})
                if len(tasks) > chunk_size*task_no:
                    return tasks[chunk_size*(task_no-1):chunk_size*task_no]