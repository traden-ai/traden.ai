import random
from Models.models.model_interface import *
from Models.model_database_handler.model_database_handler import *


class Random(ModelInterface):

    description = "Buys and sells randomly."

    input_data = {}

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0, 1)})
            output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})

        return output


if __name__ == '__main__':
    x = Random()
    save_instance("Random", x)
