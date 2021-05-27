from model_database_handler.model_database_handler import save_instance
import random
from typing import Dict
from models.model_interface import *
from model_database_handler.model_database_handler import *
from constants import PYTHON_PATH

class trend_following(ModelInterface):

    description = "Follows market trends."

    prev = {}
    prices_bought = {}

    price_increase = 0.02
    volume_increase = 0.5
    profit_target = 0.5
    stop_loss = 0.1

    def execute(self, daily_data: dict):
        output = []
        
        if (self.prev == {}):
            self.prev = daily_data
            return output

        for s in daily_data:
        
            prev_close = float(self.prev[s]["4. close"])
            prev_volume = float(self.prev[s]["5. volume"])
            close = float(daily_data[s]["4. close"])
            volume = float(daily_data[s]["5. volume"])

            pp = (close - prev_close) / prev_close
            vp = (volume - prev_volume) / prev_volume

            if (s not in self.prices_bought and pp >= self.price_increase and vp >= self.volume_increase):
                output.append(
                    {"Ticker": s, "Action": Action.BUY, "Intensity": 1})
                self.prices_bought[s] = close

            elif (s in self.prices_bought):
                pdelta = close - \
                    self.prices_bought[s] / self.prices_bought[s]
                
                #take profit
                if (pdelta >= self.profit_target):
                    output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 0.75})
                
                #stop losses
                elif (pdelta < self.stop_loss):
                    output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 1})

        self.prev = daily_data
        return output


if __name__ == '__main__':
    x = trend_following()
    save_instance("trend_following", x)
