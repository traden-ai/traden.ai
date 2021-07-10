from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.constants import MAXIMUM_DATE
from DataProvider.data_updater.data_updater_planner import DataUpdaterPlanner
from DataProvider.data_updater.data_updater_worker import DataUpdaterWorker
from DataProvider.database_handler.database_handler import DatabaseHandler
import concurrent.futures


class DataUpdater:

    def __init__(self, resource_handler, database_handler, no_workers=1):
        self.resource_handler = resource_handler
        self.database_handler = database_handler
        self.planner = DataUpdaterPlanner(database_handler, id=id)
        self.workers = []
        for i in range(no_workers):
            self.workers.append(DataUpdaterWorker(resource_handler, database_handler))

    def plan_database(self):
        self.planner.update_task_list(MAXIMUM_DATE, workers=len(self.workers))

    def update_database(self, no_tasks):
        executor = concurrent.futures.ProcessPoolExecutor(len(self.workers))
        futures = []

        tasks = self.database_handler.get_tasks(no_tasks)
        size = round(no_tasks / len(self.workers))
        for i in range(len(self.workers)):
            if tasks and len(tasks) > (i+1)*size:
                futures.append(executor.submit(self.workers[i].execute_tasks, tasks[i*size:(i+1)*size]))
        concurrent.futures.wait(futures)