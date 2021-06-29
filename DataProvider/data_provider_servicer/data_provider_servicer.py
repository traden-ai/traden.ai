from DataProviderContract.generated_files import data_provider_pb2_grpc, data_provider_pb2


class DataProviderServicer(data_provider_pb2_grpc.DataProviderServicer):
    database_handler = None
    current_stocks = None

    def __init__(self, database_handler):
        super(DataProviderServicer, self).__init__()
        self.database_handler = database_handler

    def ctrl_ping(self, request, context):
        return data_provider_pb2.CtrlPingResponse(output=request.input)

    def get_past_data(self, request, context): # TODO this can and should be otimized, this is a stream
        tickers, indicators, interval = request.tickers, request.indicators, request.interval
        start_date, end_date = interval.start_date, interval.end_date

        are_tickers_available, available_tickers, not_available_tickers = self.database_handler.are_tickers_possible(tickers)
        if not are_tickers_available:
            return data_provider_pb2.PastDataResponse(
                tickers=data_provider_pb2.TickerList(available_tickers=available_tickers, not_available_tickers=not_available_tickers),
                status=data_provider_pb2.PastDataResponse.TICKERS_NOT_AVAILABLE)

        is_date_possible, new_start_date, new_end_date = self.database_handler.is_interval_possible(tickers, indicators, start_date, end_date)
        if not is_date_possible:
            return data_provider_pb2.PastDataResponse(
                interval=data_provider_pb2.TimeInterval(start_date=new_start_date, end_date=new_end_date),
                status=data_provider_pb2.PastDataResponse.DATE_NOT_AVAILABLE)

        data = self.database_handler.get_data_by_date(tickers, indicators, start_date, end_date)
        list_day_data = []
        for date in data:
            list_ticker_data = []
            for ticker in data[date]:
                ticker_data = data_provider_pb2.TickerData(ticker=ticker, indicators_to_values=data[date][ticker])
                list_ticker_data.append(ticker_data)
            day_data = data_provider_pb2.DayData(date=date, ticker_data=list_ticker_data)
            list_day_data.append(day_data)
        stock_data = data_provider_pb2.StockData(multiple_days_data=list_day_data)
        return data_provider_pb2.PastDataResponse(data=stock_data, status=data_provider_pb2.PastDataResponse.OK)