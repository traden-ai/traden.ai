from DataProviderContract.generated_files import data_provider_pb2
from ExchangeContract.generated_files import exchange_pb2_grpc, exchange_pb2
from Models.model_database_handler.model_database_handler import list_instances, delete_instance, get_instance


class ExchangeServicer(exchange_pb2_grpc.ExchangeServicer):
    # TODO IMPLEMENT THIS

    def __init__(self, data_provider_frontend, logger):
        super(ExchangeServicer, self).__init__()
        self.data_provider_frontend = data_provider_frontend
        self.logger = logger
