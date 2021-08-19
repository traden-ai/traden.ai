from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Models.model_data_endpoint.model_data_endpoint import ModelDataEndpoint


class ModernPortfolioAllocator:
    mu = None

    S = None

    weights = None

    tickers_with_models = None

    start_date = None

    end_date = None

    data_endpoint = None

    def __init__(self, tickers_with_models, data_endpoint, start_date="2015-01-01", end_date="2021-01-01"):
        self.tickers_with_models = tickers_with_models
        self.start_date = start_date
        self.end_date = end_date
        self.data_endpoint = data_endpoint

    def process_weights(self):
        df = self.data_endpoint.get_prices_panda(list(self.tickers_with_models), self.start_date, self.end_date)
        self.mu = expected_returns.mean_historical_return(df)
        self.S = risk_models.sample_cov(df)
        self.ef = EfficientFrontier(self.mu, self.S)
        self.weights = self.ef.max_sharpe()

    def get_allocation(self, ticker):
        return self.weights[ticker]