from concurrent import futures
from multiprocessing import Process
import grpc
import sys

from DataProvider.data_resources.resource_handler.resource_handler import ResourceHandler
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.data_updater.data_updater import DataUpdater
from DataProvider.database_handler.database_handler import DatabaseHandler
from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProviderContract.generated_files.data_provider_pb2_grpc import DataProviderServicer
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
        print(f"Usage: python main.py host port [id = 1]\n")

    # Parse arguments
    host = args[1]
    port = args[2]
    id = 1 if len(args) == MAX_ARGS - 1 else int(args[MAX_ARGS - 1])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_provider_pb2_grpc.add_DataProviderServicer_to_server(
        DataProviderServicer(), server)
    server.add_insecure_port(f"{host}:{port}")

    db = DatabaseHandler()

    du = DataUpdater(ResourceHandler([AlphaVantage()], db), DatabaseHandler(), no_workers=5, id=id)

    p = Process(target=du.update_database(), args=())

    # server running
    server.start()
    p.start()
    p.join()
    server.wait_for_termination()
