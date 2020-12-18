import pandas as pd
from random import randint
from .model_interface import ModelInterface

class EMA(ModelInterface):

    def __init__(self, tradable_stocks, short=20, long=50):
        self.tickers = tradable_stocks
        self.short = short
        self.long = long
        # this way data isnt kept
        self.dfs = {}

    def preprocess_data(self, data):
        for t in self.tickers:
            hold = pd.DataFrame()
            
            values = pd.DataFrame({"close": [float(dic[t]['Close']) for dic in data]})
            ema_short = pd.DataFrame.ewm(values, span=self.short).mean()
            ema_long = pd.DataFrame.ewm(values, span=self.long).mean()
            
            #this could be better
            hold["close"] = values["close"]
            hold["short"] = ema_short["close"]
            hold["long"] = ema_long["close"]
            self.dfs[t] = hold

    def execute(self, simulation):
        ledger = simulation.get_ledger()
        balance = ledger.get_balance()
        owned_stocks = ledger.get_stocks()

        for s in owned_stocks:
            close = self.dfs[s].at[simulation.get_iteration(), 'close']
            ema_long = self.dfs[s].at[simulation.get_iteration(), 'long']

            if close < ema_long:
                simulation.sell(s, owned_stocks[s])
        
        for s in self.tickers:
            ema_short = self.dfs[s].at[simulation.get_iteration(), 'short']
            ema_long = self.dfs[s].at[simulation.get_iteration(), 'long']
            close = self.dfs[s].at[simulation.get_iteration(), 'close']

            available = balance//close

            if ema_short > ema_long:
                simulation.buy(s, randint(0, available))