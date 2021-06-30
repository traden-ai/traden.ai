from Models.models.model_interface import *
from Models.model_database_handler.model_database_handler import *


class TrendFollowing(ModelInterface):

    description = "Follows market trends."

    input_data = [TradingData.dailyAdjusted]

    prev = {}
    prices_bought = {}

    price_increase = 0.02
    volume_increase = 0.5
    profit_target = 0.5
    stop_loss = 0.1

    def execute(self, daily_data: dict):
        output = []

        if self.prev == {}:
            self.prev = daily_data
            return output

        for s in daily_data:

            prev_close = self.prev[s].dailyAdjusted.close
            prev_volume = self.prev[s].dailyAdjusted.volume
            close = daily_data[s].dailyAdjusted.close
            volume = daily_data[s].dailyAdjusted.volume

            pp = (close - prev_close) / prev_close
            vp = (volume - prev_volume) / prev_volume

            if s not in self.prices_bought and pp >= self.price_increase and vp >= self.volume_increase:
                output.append(
                    {"Ticker": s, "Action": Action.BUY, "Intensity": 1})
                self.prices_bought[s] = close

            elif s in self.prices_bought:
                pdelta = close - \
                         self.prices_bought[s] / self.prices_bought[s]

                # take profit
                if pdelta >= self.profit_target:
                    output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 0.75})

                # stop losses
                elif pdelta < self.stop_loss:
                    output.append({"Ticker": s, "Action": Action.SELL, "Intensity": 1})

        self.prev = daily_data
        return output


if __name__ == '__main__':
    x = TrendFollowing()
    save_instance("TrendFollowing", x)
