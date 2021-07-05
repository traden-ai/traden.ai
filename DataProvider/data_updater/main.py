import sys
from multiprocessing import Process

from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.data_updater import DataUpdater
from DataProvider.database_handler.database_handler import DatabaseHandler

MAX_ARGS = 2

if __name__ == '__main__':
    args = sys.argv

    # Receive and print arguments
    print(f"Received {len(args)} arguments\n")
    for i in range(len(args)):
        print(f"arg[{i}] = {args[i]}")
        print("")

    # Check arguments
    if len(args) not in (MAX_ARGS - 1, MAX_ARGS):
        print("ERROR incorrect number of arguments.")
        print(f"Usage: python main.py no_tasks [AlphaVantageKey]\n")

    # Parse arguments
    no_tasks = int(args[1])
    alpha_vantage_key = "E9NN094GU5JX53JA" if len(args) == MAX_ARGS - 1 else args[MAX_ARGS - 1]

    db = DatabaseHandler()
    du = DataUpdater(ResourceHandler([AlphaVantage(key=alpha_vantage_key)], db), DatabaseHandler(), no_workers=20)

    if no_tasks==0:
        p1 = Process(target=du.plan_database())
        p1.start()
        p1.join()
    else:
        p2 = Process(target=du.update_database(no_tasks=no_tasks))
        p2.start()
        p2.join()
