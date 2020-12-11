class Ledger:
    def __init__(self, balance, tradable_stocks):
        self.balance = balance
        self.stocks = {}
        for el in tradable_stocks:
            self.stocks[tradable_stocks] = 0
    

    def buy(self, stock_name, stock_price, amount):
        if stock_name in self.stocks and self.balance >= stock_price*amount:
            self.balance -= stock_price*amount
            self.stocks[stock_name] += amount
            return True
        else:
            return False

    def sell(self, stock_name, stock_price, amount):
        if stock_name in self.stocks and self.stocks[stock_name] >= amount:
            self.balance += stock_price*amount
            self.stocks[stock_name] -= amount
            return True
        else:
            return False
    
    def get_balance(self):
        return self.balance

    def get_stocks(self):
        return self.stocks

    def get_amount_stock(self, stock_name):
        return self.stocks(stock_name)