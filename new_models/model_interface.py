from enum import Enum


class Action(Enum):
    BUY = 1
    SELL = 2


class ModelInterface:

    tradable_tickers = []

    def set_tradable_tickers(self, tradable_tickers: list):
        """Receives Tradable Tickers"""
        self.tradable_tickers = tradable_tickers

    def execute(self, daily_data: dict) -> list:
        """Executes actions for a certain day in the respective runnable
        return should be of the form [{"Ticker": ticker, "Action": Action, "Intensity": float}, ...]
        float between 0..1 representing intensity, the intensity should be non increasing"""
        pass
