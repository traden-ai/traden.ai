import random
from Models.models.model_interface import *
from Models.model_database_handler.model_database_handler import *


class MACDCrossing(ModelInterface):

    description = "Buys and sells when MACDs cross."

    input_data = [TradingData.macd]

    prev = {}

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            macd = daily_data[s].macd.macd
            macd_signal = daily_data[s].macd.macdSignal
            diff = macd - macd_signal

            if s in self.prev:
                if diff > 0 and self.prev[s] < 0:
                    output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0.5, 1)})
                elif diff < 0 and self.prev[s] > 0:
                    output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0.5, 1)})

            self.prev[s] = diff

        return output


if __name__ == '__main__':
    x = MACDCrossing()
    save_instance("MACDCrossing", x)
