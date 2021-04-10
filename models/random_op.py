import random
from models.model_interface import *


class Random(ModelInterface):

    def execute(self, daily_data: dict):
        output = []
        for s in daily_data:
            output.append({"Ticker": s, "Action": Action.SELL, "Intensity": random.uniform(0, 1)})
            output.append({"Ticker": s, "Action": Action.BUY, "Intensity": random.uniform(0, 1)})
        return output
