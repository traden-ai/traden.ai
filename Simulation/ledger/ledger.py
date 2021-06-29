class Ledger:
    def __init__(self, balance: float, tradable_stocks: list):
        self.balance = balance
        self.stocks = {}
        for ticker in tradable_stocks:
            self.stocks[ticker] = 0

    def get_balance(self):
        return self.balance

    def get_stocks(self):
        return self.stocks

    def get_amount_stock(self, stock_name: str):
        return self.stocks[stock_name]

    def buy(self, stock_name: str, stock_price: float, amount: float, transaction_fee: float = .0):
        if stock_name in self.stocks and self.balance >= stock_price * amount:
            self.balance -= stock_price * amount
            self.stocks[stock_name] += amount * (1 - transaction_fee)
            return True
        else:
            return False

    def sell(self, stock_name: str, stock_price: float, amount: float, transaction_fee: float = .0):
        if stock_name in self.stocks and self.stocks[stock_name] >= amount:
            self.balance += stock_price * amount * (1 - transaction_fee)
            self.stocks[stock_name] -= amount
            return True
        else:
            return False

    def has_stocks(self):
        for s in self.stocks:
            if self.stocks[s] != 0:
                return True
        return False
