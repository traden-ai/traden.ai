from model_interface import ModelInterface
import pandas as pd
from random import randint

class EMA(ModelInterface):

    def __init__(self, tradable_stocks, low = 20, high = 50):
        self.tickers = tradable_stocks
        self.low = low
        self.high = high
        # this way data isnt kept
        self.dfs = {}


    def preprocess_data(self, data):
        for t in self.tickers:
            hold = pd.DataFrame()
            
            values = pd.DataFrame({"close": [float(dic[t]['Close']) for dic in data]})
            ema_low = pd.DataFrame.ewm(values, span=self.low).mean()
            ema_high = pd.DataFrame.ewm(values, span=self.high).mean()
            
            #this could be better
            hold["close"] = values["close"]
            hold["low"] = ema_low["close"]
            hold["high"] = ema_high["close"]
            self.dfs[t] = hold


    def execute(self, simulation):
        ledger = simulation.get_ledger()
        balance = ledger.get_balance()
        owned_stocks = ledger.get_stocks()

        for s in owned_stocks:
            close = self.dfs[s].at[simulation.get_iteration(), 'close']
            ema_high = self.dfs[s].at[simulation.get_iteration(), 'high']

            if close < ema_high:
                simulation.sell(s, owned_stocks[s])
        
        for s in self.tickers:
            ema_low = self.dfs[s].at[simulation.get_iteration(), 'low']
            ema_high = self.dfs[s].at[simulation.get_iteration(), 'high']
            close = self.dfs[s].at[simulation.get_iteration(), 'close']

            available = balance//close

            if ema_low > ema_high:
                simulation.buy(s, randint(0, available))