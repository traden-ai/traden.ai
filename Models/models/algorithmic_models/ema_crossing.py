import random

from enum import Enum
from Models.models.action import Action
from Models.models.trading_data import TradingData
from Models.models.model_interface import ModelInterface
from Models.model_database_handler.model_database_handler import *


class EMACrossing(ModelInterface):
    description = "Buys and sells when EMA and Close price cross."

    input_data = {TradingData.dailyAdjusted, TradingData.ema}

    buy_percentage = 1

    def execute(self, daily_data: dict):
        output = []

        for s in daily_data:
            close = daily_data[s].dailyAdjusted.adjustedClose
            ema20 = daily_data[s].ema.ema20

            if close < ema20:
                output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 1})
            if close > ema20:
                output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})

        return output, self.buy_percentage


if __name__ == '__main__':
    x = EMACrossing()
    save_instance("EMACrossing", x)
