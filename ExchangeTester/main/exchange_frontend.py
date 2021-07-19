import grpc

from ExchangeContract.generated_files import exchange_pb2_grpc


class ExchangeFrontend:

    def __init__(self, exchange_host, exchange_port):
        self.exchange_host = exchange_host
        self.exchange_port = exchange_port
        self.channel = grpc.insecure_channel(f"{exchange_host}:{exchange_port}")
        self.stub = exchange_pb2_grpc.ExchangeStub(channel=self.channel)

    def ctrl_ping(self, ctrl_ping_request):
        return self.stub.ctrl_ping(ctrl_ping_request)

    def start_model(self, start_model_request):
        return self.stub.start_model(start_model_request)

    def stop_model(self, stop_model_request):
        return self.stub.stop_model(stop_model_request)

    def add_capital_to_model(self, add_capital_to_model_request):
        return self.stub.add_capital_to_model(add_capital_to_model_request)

    def remove_capital_from_model(self, remove_capital_from_model_request):
        return self.stub.remove_capital_from_model(remove_capital_from_model_request)

    def add_tickers_to_model(self, add_tickers_to_model_request):
        return self.stub.add_tickers_to_model(add_tickers_to_model_request)

    def remove_tickers_from_model(self, remove_tickers_from_model_request):
        return self.stub.remove_tickers_from_model(remove_tickers_from_model_request)

    def ledger_info(self, ledger_info_request):
        return self.stub.ledger_info(ledger_info_request)

    def model_info(self, model_info_request):
        return self.stub.model_info(model_info_request)
