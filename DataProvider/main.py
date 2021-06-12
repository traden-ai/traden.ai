import futures as futures
import grpc
import sys

from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProviderContract.generated_files.data_provider_pb2_grpc import DataProviderServicer

if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 3:
        workers = args[1]
        port = args[2]
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
        data_provider_pb2_grpc.add_DataProviderServicer_to_server(
            DataProviderServicer(), server)
        server.add_insecure_port("[::]:{}".format(port))  # TODO change server port to be reachable, this should be a secure_port however this requires ssl creds
        server.start()
        server.wait_for_termination()


# TODO the continuous update of the db should be done by a different process started here