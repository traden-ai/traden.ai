class Ledger:
    def __init__(self, balance: float, tradable_stocks: list):
        self.balance = balance
        self.stocks = {}
        for el in tradable_stocks:
            self.stocks[el] = 0
    

    def buy(self, stock_name: str, stock_price: float, amount: int):
        if stock_name in self.stocks and self.balance >= stock_price*amount:
            self.balance -= stock_price*amount
            self.stocks[stock_name] += amount
            return True
        else:
            return False

    def sell(self, stock_name: str, stock_price: float, amount: int):
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

    def get_amount_stock(self, stock_name: str):
        return self.stocks[stock_name]