import numpy as np
import pandas as pd

from DataProviderContract.generated_files import data_provider_pb2_grpc
from DataProviderContract.generated_files import data_provider_pb2
from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Simulation.simulation_servicer.utils import data_load
from utils.data_distribution import convert_data_points_2D_into_percentile_2D, convert_data_points_into_percentile_list
from utils.utils import convert_data_to_np, convert_prices_to_np, convert_nominal_to_variation_2D, \
    convert_nominal_to_variation_1D


class ModelDataEndpoint:
    data_provider_frontend = None

    def __init__(self, data_provider_frontend):
        self.data_provider_frontend = data_provider_frontend

    def get_past_data(self, tickers, indicators, start_date, end_date):
        request = data_provider_pb2.PastDataRequest(tickers=tickers, indicators=indicators,
                                                    interval=data_provider_pb2.TimeInterval(start_date=start_date,
                                                                                            end_date=end_date))
        response, status = self.data_provider_frontend.get_past_data(request)
        dates, data, prices = data_load(response["data"])
        if status != data_provider_pb2.PastDataResponse.OK:
            return None, None, None, status
        return dates, data, prices, status

    def get_data_np(self, tickers, indicators, start_date, end_date):
        _, data, _, _ = self.get_past_data(tickers, indicators, start_date, end_date)
        return convert_data_to_np(data)

    def get_variation_data_np(self, tickers, indicators, start_date, end_date):
        data = self.get_data_np(tickers, indicators, start_date, end_date)
        data_variations = {}
        for ticker in tickers:
            data_variations[ticker] = np.array(convert_nominal_to_variation_2D(data[ticker]))
        return data_variations

    def get_percentile_variation_data_np(self, tickers, indicators, start_date, end_date):
        data_variations = self.get_variation_data_np(tickers, indicators, start_date, end_date)
        data_percentiles = {}
        x_dist = {}
        for ticker in tickers:
            data_percentiles[ticker], x_dist[ticker] = convert_data_points_2D_into_percentile_2D(data_variations[ticker])
        return data_percentiles, x_dist

    def get_prices_np(self, tickers, start_date, end_date):
        _, _, prices, _ = self.get_past_data(tickers, ["dailyAdjusted"], start_date, end_date)
        return convert_prices_to_np(prices)

    def get_variation_prices_np(self, tickers, start_date, end_date):
        prices = self.get_prices_np(tickers, start_date, end_date)
        price_variations = {}
        for stock in prices:
            price_variations[stock] = convert_nominal_to_variation_1D(prices[stock])
        return price_variations

    def get_percentile_variation_prices_np(self, tickers, start_date, end_date):
        prices_variation = self.get_variation_prices_np(tickers, start_date, end_date)
        percentile_prices = {}
        y_dist = {}
        for ticker in tickers:
            percentile_prices[ticker], y_dist[ticker] = convert_data_points_into_percentile_list(list(prices_variation[ticker]))
            percentile_prices[ticker].transpose()
        return percentile_prices, y_dist

    def get_prices_panda(self, tickers, start_date, end_date):
        dates, _, prices, _ = self.get_past_data(tickers, ["dailyAdjusted"], start_date, end_date)
        prices = convert_prices_to_np(prices)
        arr = []
        for ticker in tickers:
            arr.append(prices[ticker].flatten())
        prices = pd.DataFrame(np.stack(arr).transpose(), index=dates, columns=tickers)
        return prices
