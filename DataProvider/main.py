import sys
import grpc
import logging
from concurrent import futures

from DataProvider.database_handler.database_handler import DatabaseHandler
from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProvider.data_provider_servicer.data_provider_servicer import DataProviderServicer

MAX_ARGS = 4

if __name__ == '__main__':
    args = sys.argv

    # receive and print arguments
    print(f"Received {len(args)} arguments\n")
    for i in range(len(args)):
        print(f"arg[{i}] = {args[i]}\n")

    # check arguments
    if len(args) not in (MAX_ARGS - 1, MAX_ARGS):
        print("ERROR incorrect number of arguments.")
        print(f"Usage: python3 main.py host port [workers = 10]\n")
        exit()

    # parse arguments
    host = args[1]
    port = args[2]
    workers = 10 if len(args) == MAX_ARGS - 1 else args[MAX_ARGS - 1]

    # setup server logger
    logger = logging.getLogger("data_provider")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler = logging.FileHandler("data_provider.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # server setup
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    data_provider_pb2_grpc.add_DataProviderServicer_to_server(DataProviderServicer(DatabaseHandler(), logger), server)
    server.add_insecure_port(f"{host}:{port}")

    try:
        # server running
        server.start()
        logger.info("Server running and waiting for clients...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Terminating...")
        exit()
