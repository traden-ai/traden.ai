from DataProvider.data_updater.constants import MINIMUM_DATE, MAXIMUM_DATE
from DataProvider.data_updater.utils import get_current_date


class DataUpdaterWorker:

    def __init__(self, resource_handler, database_handler):
        self.resource_handler = resource_handler
        self.database_handler = database_handler

    def execute_task(self, task, confirmation=True): # TODO confirmation is a way of veryfing if the task was succefully accomplished or not
        print("Started executing task for ticker {}, and indicator {}".format(task["Ticker"], task["Indicator"]))
        if task["StartDate"] == None and task["EndDate"] == None:
            items = self.resource_handler.get_past_data([task["Ticker"]], [task["Indicator"]], MINIMUM_DATE, get_current_date())
        else:
            items = self.resource_handler.get_past_data([task["Ticker"]], [task["Indicator"]], task["StartDate"], task["EndDate"])
        self.database_handler.update_data(items)
        print("Finished executing task for ticker {}, and indicator {}".format(task["Ticker"], task["Indicator"]))

    def execute_tasks(self, tasks, confirmation=True):
        for task in tasks:
            self.execute_task(task, confirmation=confirmation)