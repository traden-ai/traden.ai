from random import randint
from .model_interface import ModelInterface


class Random(ModelInterface):

    def __init__(self, tradable_stocks):
        self.tickers = tradable_stocks

    def execute(self, simulation):
        ledger = simulation.get_ledger()
        balance = ledger.get_balance()
        owned_stocks = ledger.get_stocks()

        if randint(0, 1):
            for s in self.tickers:
                close = simulation.get_prices(s)[simulation.get_iteration()]
                available = balance // close
                simulation.buy(s, randint(0, available))
        else:
            for s in owned_stocks:
                simulation.sell(s, owned_stocks[s])
