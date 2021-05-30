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
    percentage_threshold = None
    nominal_threshold = None

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
            price = float(getattr(daily_data[ticker], "close"))
            difference = estimation - price
            if self.percentage_threshold:
                if difference > (self.percentage_threshold * price):
                    output.append({"Ticker": ticker, "Action": Action.BUY,
                                   "Intensity": min(abs(difference) / (2 * (self.percentage_threshold * price)), 1)})
                elif difference < (-self.percentage_threshold * price):
                    output.append({"Ticker": ticker, "Action": Action.SELL,
                                   "Intensity": min(abs(difference) / (2 * (self.percentage_threshold * price)), 1)})
            elif self.nominal_threshold:
                if difference > self.nominal_threshold:
                    output.append({"Ticker": ticker, "Action": Action.BUY,
                                   "Intensity": min(abs(difference) / (2 * self.nominal_threshold), 1)})
                elif difference < -self.nominal_threshold:
                    output.append({"Ticker": ticker, "Action": Action.SELL,
                                   "Intensity": min(abs(difference) / (2 * self.nominal_threshold), 1)})
        return output

    def set_threshold(self, percentage_threshold=None, nominal_threshold=None):
        self.percentage_threshold = percentage_threshold
        self.nominal_threshold = nominal_threshold

    def get_estimations(self):
        return self.estimations
