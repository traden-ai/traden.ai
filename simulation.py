from ledger.py import Ledger
from stock_database.py import load

class Simulation:
    def __init__(self, balance, tradable_stocks, start_date, end_date, selling_model, buying_model):
        self.initial_balance = balance
        
        self.ledger = Ledger(balance, tradable_stocks)
        self.tradable_stocks = tradable_stocks

        self.start_date = start_date
        self.current_date = start_date
        self.iterator = 0
        self.end_date = end_date
        
        self.selling_model = selling_model
        self.buying_model = buying_model
        
        self.logs = []
        self.data = load(self.tradable_stocks, self.start_date, self.end_date)

    def execute():
        while (self.current_date != self.end_date):
            selling_model()
            buying_model()
            self.current_date = adding_days_to_date(self.current_date, 1)
            self.iterator += 1
        self.iterator -= 1
        self.sell_all()
        return self.ledger.balance - self.initial_balance

    def buy(stock_name, amount):
        stock_price = self.data[iterator][stock_name]["Close"]
        isPossible = self.ledger.buy(stock_name, stock_price, amount)
        if isPossible:
            self.logs.extend({"action":"Bought", "date": self.current_date, "stock_name": stock_name, "stock_price": stock_price, "amount": amount})

    def sell(stock_name, amount):
        stock_price = self.data[iterator][stock_name]["Close"]
        isPossible = self.ledger.sell(stock_name, stock_price, amount)
        if isPossible:
            self.logs.extend({"action":"Sold", "date": self.current_date, "stock_name": stock_name, "stock_price": stock_price, "amount": amount})

    def sell_all():
        stocks = self.ledger.get_stocks()
        for stock in stocks:
            sell(stock, stocks[stock])

    def logs_str():
        logs_format = ""
        for log in self.logs:
            logs_format += "{} {} stocks of {} with price {} at {}\n".format(log["action"], log["amount"], log["stock_name"], log["stock_price"], log["date"])
        return logs_format
