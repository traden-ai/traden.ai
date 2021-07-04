import unittest

from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from DataProviderContract.generated_files import data_provider_pb2
from DataProviderTester.test.constants import DP_HOST, DP_PORT


class DataProviderTestMethods(unittest.TestCase):
    PING_MESSAGE = "Test"

    VALID_START_DATE = "2020-01-01"
    VALID_END_DATE = "2021-01-01"

    VALID_INDICATOR_LIST = ["bbands", "macd"]
    VALID_TICKER_LIST = ["FOX", "HCA"]

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
        responses = self.client.get_past_data(request)
        for response in responses:
            print(response)
            self.assertEqual(response.status, data_provider_pb2.PastDataResponse.OK)
            for day_data in response.multiple_day_data:
                self.assertEqual(len(day_data.date.split("-")), 3)
                for ticker_data in day_data.ticker_data:
                    self.assertIn(ticker_data.ticker, self.VALID_TICKER_LIST)
                    for indicator in ticker_data.indicators_to_values:
                        self.assertIn(indicator, self.VALID_INDICATOR_LIST)
                        self.assertNotEqual(ticker_data.indicators_to_values[indicator], None)

    def test_get_past_data_without_valid_tickers(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.VALID_START_DATE, end_date=self.VALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.INVALID_TICKER_LIST,
                                                    indicators=self.VALID_INDICATOR_LIST, interval=time_interval)
        responses = self.client.get_past_data(request)
        for response in responses:
            self.assertEqual([], response.tickers.available_tickers)
            for ticker in response.tickers.not_available_tickers:
                self.assertIn(ticker, self.INVALID_TICKER_LIST)
            self.assertEqual(response.status, data_provider_pb2.PastDataResponse.TICKERS_NOT_AVAILABLE)

    def test_get_past_data_without_valid_indicators(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.VALID_START_DATE, end_date=self.VALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.VALID_TICKER_LIST, indicators=self.INVALID_INDICATOR_LIST, interval=time_interval)
        responses = self.client.get_past_data(request)
        for response in responses:
            self.assertEqual(response.status, data_provider_pb2.PastDataResponse.NOK)

    def test_get_past_data_without_valid_dates(self):
        time_interval = data_provider_pb2.TimeInterval(start_date=self.INVALID_START_DATE, end_date=self.INVALID_END_DATE)
        request = data_provider_pb2.PastDataRequest(tickers=self.VALID_TICKER_LIST,
                                                    indicators=self.VALID_INDICATOR_LIST, interval=time_interval)
        responses = self.client.get_past_data(request)
        for response in responses:
            self.assertEqual(response.status, data_provider_pb2.PastDataResponse.INTERVAL_NOT_AVAILABLE)



if __name__ == '__main__':
    unittest.main()
