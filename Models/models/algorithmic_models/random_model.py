import random

from enum import Enum
from Models.models.action import Action
from Models.models.model_interface import ModelInterface
from Models.model_database_handler.model_database_handler import *


class Random(ModelInterface):

    description = "Buys and sells randomly."

    input_data = {}

    buy_percentage = 1

    def execute(self, daily_data: dict):

        output = []

        for s in daily_data:
            output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0, 1)})
            output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})

        return output, self.buy_percentage


if __name__ == '__main__':
    x = Random()
    save_instance("Random", x)
