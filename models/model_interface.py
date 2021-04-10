from enum import Enum


class Action(Enum):
    BUY = 1
    SELL = 2


class ModelInterface:

    def execute(self, daily_data: dict) -> list:
        """Executes actions for a certain day in the respective runnable
        ----------------------------------------------------------------------------------
        Daily_data  is of the form
        {Tradable_ticker_1: {"RSI" : 54.7352, ...}}
        ----------------------------------------------------------------------------------
        Output List is of the form
        [{"Ticker": ticker, "Action": Action, "Intensity": float}, ...]
        float between 0..1 representing intensity, the intensity should be non increasing
        """
        pass
