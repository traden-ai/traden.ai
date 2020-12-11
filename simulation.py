from ledger.py import Ledger

class Simulation:
    def __init__(self, balance, tradable_stocks, no_months, model):
        self.ledger = Ledger(balance, tradable_stocks)
        self        
