import random
from models.model_interface import *
from model_database_handler.model_database_handler import *


class RSISignals(ModelInterface):

    description = "Buys and sells as RSI indicates gives oversold and overbought signals."

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            rsi = daily_data[s].rsi

            if rsi < 33.3:
                output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0.5, 1)})
            elif rsi > 66.6:
                output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0.5, 1)})

        return output


if __name__ == '__main__':
    x = RSISignals()
    save_instance("RSISignals", x)
