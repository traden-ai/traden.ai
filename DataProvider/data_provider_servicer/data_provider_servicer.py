from DataProviderContract.generated_files import data_provider_pb2_grpc, data_provider_pb2

class DataProviderServicer(data_provider_pb2_grpc.DataProviderServicer):

    def ctrl_ping(self, request, context):
        return data_provider_pb2.CtrlPingResponse(output=request.input)

    def get_past_data(self, request, context):
        tickers, indicators, interval = request.tickers, request.indicators, request.interval
        truth_value, init_date, end_date = is_interval_possible(tickers, indicators, interval):
        if truth_value:
            # return data between init_date and end_date for tickers and indicators
        else:
            return data_provider_pb2.PastDataResponse(interval=data_provider_pb2.TimeInterval(initial_date=init_date, end_date=end_date), status=data_provider_pb2.PastDataResponse.NOK)

