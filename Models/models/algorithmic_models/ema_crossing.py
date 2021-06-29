import random
from Models.models.model_interface import *
from Models.model_database_handler.model_database_handler import *


class EMACrossing(ModelInterface):

    description = "Buys and sells when EMA and Close price cross."

    input_data = [InputData.PRICE_DATA, InputData.TECHNICAL_INDICATORS]

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            close = daily_data[s].close
            ema = daily_data[s].technical_indicators.ema

            if close < ema:
                output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 1})

        for s in daily_data:
            close = daily_data[s].close
            ema = daily_data[s].ema

            if close > ema:
                output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})

        return output


if __name__ == '__main__':
    x = EMACrossing()
    save_instance("EMACrossing", x)
