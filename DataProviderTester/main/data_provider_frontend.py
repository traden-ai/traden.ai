import grpc

from DataProviderContract.generated_files import data_provider_pb2_grpc


class DataProviderFrontend:

    def __init__(self, data_provider_host, data_provider_port):
        self.data_provider_host = data_provider_host
        self.data_provider_port = data_provider_port
        self.channel = grpc.insecure_channel(f"{data_provider_host}:{data_provider_port}")
        self.stub = data_provider_pb2_grpc.DataProviderStub(channel=self.channel)

    def ctrl_ping(self, ctrl_ping_request):
        return self.stub.ctrl_ping(ctrl_ping_request)

    def get_past_data(self, get_past_data_request):
        return self.stub.get_past_data(get_past_data_request)

    '''
    def get_daily_data(self, get_daily_data_request):
        return self.stub.get_daily_data(get_daily_data_request)
        
    def get_intra_daily_data(self, get_intra_daily_data_request):
        return self.stub.get_intra_daily_data(get_intra_daily_data_request)
    '''

    def close(self):
        self.channel.close()
