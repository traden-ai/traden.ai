from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.constants import MAX_DATE
from DataProvider.data_updater.data_updater_planner import DataUpdaterPlanner
from DataProvider.data_updater.data_updater_worker import DataUpdaterWorker
from DataProvider.database_handler.database_handler import DatabaseHandler


class DataUpdater:

    def __init__(self, resource_handler, database_handler, no_workers=1):
        self.resource_handler = resource_handler
        self.database_handler = database_handler
        self.planner = DataUpdaterPlanner(database_handler)
        self.workers = []
        for i in range(no_workers):
            self.workers.append(DataUpdaterWorker(resource_handler, database_handler))

    def update_database(self, chunk_size=5):
        for i in range(len(self.workers)):
            tasks = self.planner.get_tasks(MAX_DATE, id=i+1, chunk_size=chunk_size)
            for task in tasks:
                self.workers[i].execute_task(task)


if __name__=="__main__":
    db_handler = DatabaseHandler()
    du = DataUpdater(ResourceHandler([AlphaVantage()], DatabaseHandler()), DatabaseHandler())
    du.update_database()