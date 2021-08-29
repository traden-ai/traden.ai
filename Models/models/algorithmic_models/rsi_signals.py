import random

from enum import Enum
from Models.models.daily_data_related.action import Action
from Models.models.daily_data_related.trading_data import TradingData
from Models.models.interfaces.model_interface import ModelInterface
from Models.model_database_handler.model_database_handler import *


class RSISignals(ModelInterface):

    description = "Buys and sells as RSI indicates gives oversold and overbought signals."

    input_data = {TradingData.rsi}

    buy_percentage = 1

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            rsi = daily_data[s].rsi.rsi

            if rsi < 33.3:
                output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0.5, 1)})
            elif rsi > 66.6:
                output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0.5, 1)})

        return output, self.buy_percentage


if __name__ == '__main__':
    x = RSISignals()
    save_instance("RSISignals", x)
