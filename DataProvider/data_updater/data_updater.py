from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.constants import MAXIMUM_DATE
from DataProvider.data_updater.data_updater_planner import DataUpdaterPlanner
from DataProvider.data_updater.data_updater_worker import DataUpdaterWorker
from DataProvider.database_handler.database_handler import DatabaseHandler
import concurrent.futures


class DataUpdater:

    def __init__(self, resource_handler, database_handler, no_workers=1, id=1):
        self.id = id
        self.resource_handler = resource_handler
        self.database_handler = database_handler
        self.planner = DataUpdaterPlanner(database_handler, id=id)
        self.workers = []
        for i in range(no_workers):
            self.workers.append(DataUpdaterWorker(resource_handler, database_handler))

    def update_database(self, chunk_size=30):
        executor = concurrent.futures.ProcessPoolExecutor(len(self.workers))
        while True:
            futures = []
            for i in range(len(self.workers)):
                tasks = self.planner.get_tasks(MAXIMUM_DATE, chunk_size=chunk_size, worker=self.id+i)
                if tasks:
                    futures.append(executor.submit(self.workers[i].execute_tasks, tasks))
            concurrent.futures.wait(futures)