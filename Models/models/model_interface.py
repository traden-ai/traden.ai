from enum import Enum


class Action(Enum):
    BUY = 1
    SELL = 2


class TradingData(Enum):
    dailyAdjusted = 1
    sma = 3
    ema = 2
    macd = 4
    rsi = 5
    vwap = 6
    cci = 7
    adx = 8
    stoch = 9
    aroon = 10
    bbands = 11
    ad = 12
    obv = 13
    companyOverview = 14
    earnings = 15
    cashFlow = 16
    balanceSheet = 17
    incomeStatement = 18


class ModelInterface:

    description = "default description for model"

    input_data = []

    def get_description(self):
        return self.description

    def get_input_data(self):
        return self.input_data

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

    def save_attributes(self) -> None:
        """Saves class attributes if needed for serialization purposes,
        for more information check jsonpickle restrictions"""
        pass

    def retrieve_attributes(self) -> None:
        """Retrieves class attributes if needed for deserialization purposes,
        this function should work as the inverse of save_attributes"""
        pass
