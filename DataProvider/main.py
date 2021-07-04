from concurrent import futures
from multiprocessing import Process
import grpc
import sys

from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.data_updater import DataUpdater
from DataProvider.database_handler.database_handler import DatabaseHandler
from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProvider.data_provider_servicer.data_provider_servicer import DataProviderServicer

MAX_ARGS = 4

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
        print(f"Usage: python main.py host port [workers = 10]\n")

    # Parse arguments
    host = args[1]
    port = args[2]
    workers = 10 if len(args) == MAX_ARGS - 1 else args[MAX_ARGS - 1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    db = DatabaseHandler()

    data_provider_pb2_grpc.add_DataProviderServicer_to_server(
        DataProviderServicer(db), server)
    server.add_insecure_port(f"{host}:{port}")

    # server running
    server.start()
    server.wait_for_termination()
