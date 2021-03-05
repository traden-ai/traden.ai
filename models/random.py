import pandas as pd
from random import randint
from .model_interface import ModelInterface

class Random(ModelInterface):

    def __init__(self, tradable_stocks):
        self.tickers = tradable_stocks
        self.dfs = {}

    def execute(self, simulation):
        ledger = simulation.get_ledger()
        balance = ledger.get_balance()
        owned_stocks = ledger.get_stocks()

        if randint(0, 1):
            for s in self.tickers:
                close = self.dfs[s].at[simulation.get_iteration(), 'close']
                available = balance//close
                simulation.buy(s, randint(0, available))
        else:
            for s in owned_stocks:
                simulation.sell(s, owned_stocks[s])
        