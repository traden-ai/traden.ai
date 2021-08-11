import grpc

from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProviderContract.generated_files import data_provider_pb2


class DataProviderFrontend:

    def __init__(self, data_provider_host, data_provider_port):
        self.data_provider_host = data_provider_host
        self.data_provider_port = data_provider_port
        self.channel = grpc.insecure_channel(f"{data_provider_host}:{data_provider_port}")
        self.stub = data_provider_pb2_grpc.DataProviderStub(channel=self.channel)

    def ctrl_ping(self, ctrl_ping_request):
        return self.stub.ctrl_ping(ctrl_ping_request)

    def get_past_data(self, get_past_data_request):
        clean_response, status = {"data": []}, None
        stream = self.stub.get_past_data(get_past_data_request)

        for response in stream:
            status = response.status if not status else status
            if status == data_provider_pb2.PastDataResponse.Status.OK:
                clean_response["data"] += response.data.multiple_days_data
            elif status == data_provider_pb2.PastDataResponse.Status.INTERVAL_NOT_AVAILABLE:
                clean_response["interval"] = response.interval
            elif status == data_provider_pb2.PastDataResponse.Status.TICKERS_NOT_AVAILABLE:
                clean_response["tickers"] = response.tickers
            else:
                return stream, status

        return clean_response, status

    '''
    def get_daily_data(self, get_daily_data_request):
        return self.stub.get_daily_data(get_daily_data_request)
        
    def get_intra_daily_data(self, get_intra_daily_data_request):
        return self.stub.get_intra_daily_data(get_intra_daily_data_request)
    '''

    def close(self):
        self.channel.close()
