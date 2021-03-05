from random import randint
from .model_interface import ModelInterface

class EMA(ModelInterface):

    def __init__(self, tradable_stocks):
        self.tickers = tradable_stocks

    def execute(self, simulation):
        ledger = simulation.get_ledger()
        balance = ledger.get_balance()
        owned_stocks = ledger.get_stocks()

        for s in owned_stocks:
            close = simulation.get_prices(s)[simulation.get_iteration()]
            ema_long = simulation.get_data_by_ticker(s)[simulation.get_iteration(), 10]   # TODO fix ugly constant

            if close < ema_long:
                simulation.sell(s, owned_stocks[s])
        
        for s in self.tickers:
            ema_short = simulation.get_data_by_ticker(s)[simulation.get_iteration(), 9] # TODO fix ugly constant
            ema_long = simulation.get_data_by_ticker(s)[simulation.get_iteration(), 10] # TODO fix ugly constant
            close = simulation.get_prices(s)[simulation.get_iteration()]

            available = balance//close

            if ema_short > ema_long:
                simulation.buy(s, randint(0, available))