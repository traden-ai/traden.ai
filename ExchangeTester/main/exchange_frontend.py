import grpc

from ExchangeContract.generated_files import exchange_pb2_grpc


class ExchangeFrontend:

    def __init__(self, data_provider_host, data_provider_port):
        self.data_provider_host = data_provider_host
        self.data_provider_port = data_provider_port
        self.channel = grpc.insecure_channel(
            f"{data_provider_host}:{data_provider_port}")
        self.stub = exchange_pb2_grpc.ExchangeStub(
            channel=self.channel)

    def ctrl_ping(self, ctrl_ping_request):
        return self.stub.ctrl_ping(ctrl_ping_request)

    def start_model(self, start_model_request):
        return self.stub.start_model(start_model_request)

    def stop_model(self, stop_model_request):
        return self.stub.stop_model(stop_model_request)

    def add_capital(self, add_capital_request):
        return self.stub.add_capital(add_capital_request)

    def remove_capital(self, remove_capital_request):
        return self.stub.remove_capital(remove_capital_request)

    def ledger_info(self, ledger_info_request):
        return self.stub.ledger_info(ledger_info_request)

    def model_info(self, model_info_request):
        return self.stub.model_info(model_info_request)

    def close(self):
        self.channel.close()
