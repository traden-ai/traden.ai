import grpc
import sys
import logging
from concurrent import futures

from SimulationContract.generated_files import simulation_pb2_grpc
from Simulation.simulation_servicer.simulation_servicer import SimulationServicer
from DataProviderTester.main.data_provider_frontend import DataProviderFrontend

MAX_ARGS = 6

if __name__ == '__main__':
    args = sys.argv

    # receive and print arguments
    print(f"Received {len(args)} arguments\n")
    for i in range(len(args)):
        print(f"arg[{i}] = {args[i]}\n")

    # check arguments
    if len(args) not in (MAX_ARGS - 1, MAX_ARGS):
        print("ERROR incorrect number of arguments.")
        print(f"Usage: python3 main.py data_provider_host data_provider_port host port [maxWorkers = 10]\n")

    # parse arguments
    data_provider_host = args[1]
    data_provider_port = args[2]
    host = args[3]
    port = args[4]
    workers = 10 if len(args) == MAX_ARGS - 1 else args[MAX_ARGS - 1]
    
    # setup server logger
    logger = logging.getLogger("simulation")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler = logging.FileHandler("simulation.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # server set up
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    data_provider_frontend = DataProviderFrontend(data_provider_host, data_provider_port)
    simulation_pb2_grpc.add_SimulationServicer_to_server(SimulationServicer(data_provider_frontend, logger), server)
    # FIXME change server port to be reachable, this should be a secure_port however this requires ssl credentials
    server.add_insecure_port(f"{host}:{port}")

    try:
        # server running
        server.start()
        logger.info("Server running and waiting for clients...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        data_provider_frontend.close()
