import grpc
import sys
from concurrent import futures

from SimulationContract.generated_files import simulation_pb2_grpc
from Simulation.simulation_servicer.simulation_servicer import SimulationServicer
from Simulation.data_provider_frontend.data_provider_frontend import DataProviderFrontend

MAX_ARGS = 6

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
        print(f"Usage: python main.py data_provider_host data_provider_port host port [maxWorkers = 10]\n")

    # Parse arguments
    data_provider_host = args[1]
    data_provider_port = args[2]
    host = args[3]
    port = args[4]
    workers = 10 if len(args) == MAX_ARGS - 1 else args[MAX_ARGS - 1]

    # server set up
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    data_provider_frontend = DataProviderFrontend(data_provider_host, data_provider_port)
    simulation_pb2_grpc.add_SimulationServicer_to_server(SimulationServicer(data_provider_frontend), server)
    # TODO change server port to be reachable, this should be a secure_port however this requires ssl creds
    server.add_insecure_port(f"{host}:{port}")

    # server running
    server.start()
    server.wait_for_termination()

    # finally
    data_provider_frontend.close()
