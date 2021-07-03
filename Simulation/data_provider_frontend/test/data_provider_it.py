import unittest

from Simulation.data_provider_frontend.data_provider_frontend import DataProviderFrontend
from DataProviderContract.generated_files import data_provider_pb2
from Simulation.data_provider_frontend.test.constants import DP_HOST, DP_PORT


class DataProviderTestMethods(unittest.TestCase):
    PING_MESSAGE = "Test"

    VALID_START_DATE = "2020-01-01"
    VALID_END_DATE = "2021-01-01"

    VALID_INDICATOR_LIST = ["bbands", "macd"]
    VALID_TICKER_LIST = ["AMZN", "MSFT"]

    INVALID_INDICATOR_LIST = ["invalid", "not_indicator"]
    INVALID_TICKER_LIST = ["invalid", "not_ticker"]

    INVALID_START_DATE = "2800-01-01"
    INVALID_END_DATE = "2900-01-01"

    client = DataProviderFrontend(DP_HOST, DP_PORT)

    def test_ctrl_ping(self):
        request = data_provider_pb2.CtrlPingRequest(input=self.PING_MESSAGE)
        response = self.client.ctrl_ping(request)
        self.assertEqual(self.PING_MESSAGE, response.output)

    def test_get_past_data_successfully(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.VALID_START_DATE, end_date=self.VALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.VALID_TICKER_LIST, indicators=self.VALID_INDICATOR_LIST, interval=time_interval)
        response = self.client.get_past_data(request)

    def test_get_past_data_without_valid_tickers(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.VALID_START_DATE, end_date=self.VALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.INVALID_TICKER_LIST,
                                                    indicators=self.VALID_INDICATOR_LIST, interval=time_interval)
        response = self.client.get_past_data(request)

    def test_get_past_data_without_valid_indicators(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.VALID_START_DATE, end_date=self.VALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.VALID_TICKER_LIST, indicators=self.INVALID_INDICATOR_LIST, interval=time_interval)
        response = self.client.get_past_data(request)

    def test_get_past_data_without_valid_dates(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.INVALID_START_DATE, end_date=self.INVALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.VALID_TICKER_LIST,
                                                    indicators=self.VALID_INDICATOR_LIST, interval=time_interval)
        response = self.client.get_past_data(request)