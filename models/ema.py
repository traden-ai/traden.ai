import random
from models.model_interface import *


class EMA(ModelInterface):

    description = "Buys and sells when EMA lines cross."

    def execute(self, daily_data: dict):
        output = []
        for s in daily_data:
            close = daily_data[s]["CLOSE"]
            ema_long = daily_data[s]["EMA50"]

            if close < ema_long:
                output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 1})

        for s in daily_data:
            ema_short = daily_data[s]["EMA20"]
            ema_long = daily_data[s]["EMA50"]

            if ema_short > ema_long:
                output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})

        return output
