from enum import Enum
from models.model_interface import ModelInterface, Action


def record_estimation(func):
    def wrapper(*args):
        daily_estimations = func(*args)
        args[0].estimations.append(daily_estimations)
        return daily_estimations

    return wrapper


class EstimatorInterface(ModelInterface):
    estimations = []
    buy_percentual_threshold = None
    sell_percentual_threshold = None
    buy_nominal_threshold = None
    sell_nominal_threshold = None

    def estimate(self, daily_data: dict) -> dict:
        """Estimates prices for a certain day in the respective runnable
        Note: the decorator should be used in order to record the estimations
        ----------------------------------------------------------------------------------
        Daily_data  is of the form
        {Tradable_ticker_1: {"RSI" : 54.7352, ...}}
        ----------------------------------------------------------------------------------
        Output is of the form
        {ticker : estimate, ...}
        """
        pass

    def execute(self, daily_data: dict) -> list:
        output = []
        results = self.estimate(daily_data)
        for ticker in results:
            estimation = results[ticker]
            price = float(daily_data[ticker].close)
            difference = estimation - price
            if self.buy_percentual_threshold != None and self.sell_percentual_threshold != None:
                if difference > (self.buy_percentual_threshold * price):
                    output.append({"Ticker": ticker, "Action": Action.BUY,
                                   "Intensity": min(abs(difference) / (2 * (self.buy_percentual_threshold * price)), 1)})
                elif difference < (-self.sell_percentual_threshold * price):
                    output.append({"Ticker": ticker, "Action": Action.SELL,
                                   "Intensity": min(abs(difference) / (2 * (self.sell_percentual_threshold * price)), 1)})
            elif self.buy_nominal_threshold != None and self.sell_nominal_threshold != None:
                if difference > self.buy_nominal_threshold:
                    output.append({"Ticker": ticker, "Action": Action.BUY,
                                   "Intensity": min(abs(difference) / (2 * self.buy_nominal_threshold), 1)})
                elif difference < -self.sell_nominal_threshold:
                    output.append({"Ticker": ticker, "Action": Action.SELL,
                                   "Intensity": min(abs(difference) / (2 * self.sell_nominal_threshold), 1)})
        return output

    def set_threshold(self, buy_percentual_threshold=None, sell_percentual_threshold=None, buy_nominal_threshold=None, sell_nominal_threshold=None):
        self.buy_percentual_threshold = buy_percentual_threshold
        self.sell_percentual_threshold = sell_percentual_threshold
        self.buy_nominal_threshold = buy_nominal_threshold
        self.sell_nominal_threshold = sell_nominal_threshold

    def get_estimations(self):
        return self.estimations

    def reset_estimations(self):
        self.estimations = []
