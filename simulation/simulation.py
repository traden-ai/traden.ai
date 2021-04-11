from data.stock_database import data_load
from utils.utils import profit_percentage_by_year, time_between_days, get_year, get_month
import matplotlib.pyplot as plt
from models.runnable_interface import *


class Simulation(Runnable):

    def __init__(self, balance: float, tradable_stocks: list, start_date: str, end_date: str, model: ModelInterface):
        super().__init__(balance, tradable_stocks, model)
        self.initial_balance = balance
        self.data, self.dates, self.prices = data_load(tradable_stocks, start_date, end_date)

        self.start_date = start_date
        self.end_date = self.dates[-1]
        self.current_date = start_date
        self.iterator = 0

        self.evaluations = []

        for date in self.dates:
            self.evaluations.append((date, []))

        self.results = []

        self.logs = []

    def execute(self, no_executions=1):
        for i in range(no_executions):
            while self.current_date != self.end_date:
                self.execute_day()
                self.current_date = self.dates[self.iterator]
                self.evaluations[self.iterator][1].append(self.get_current_value())
                self.iterator += 1
            self.iterator -= 1
            self.current_date = self.dates[self.iterator]
            self.sell_all()
            self.store_result()

    def buy(self, stock_name: str, amount: int):
        if amount > 0:
            stock_price = self.get_current_stock_price(stock_name)
            is_possible = self.ledger.buy(stock_name, stock_price, amount)
            if is_possible:
                self.logs.append({"action": "Bought", "date": self.current_date, "stock_name": stock_name,
                                  "stock_price": stock_price, "amount": amount})

    def sell(self, stock_name: str, amount: int):
        if amount > 0:
            stock_price = self.get_current_stock_price(stock_name)
            is_possible = self.ledger.sell(stock_name, stock_price, amount)
            if is_possible:
                self.logs.append(
                    {"action": "Sold", "date": self.current_date, "stock_name": stock_name,
                     "stock_price": stock_price,
                     "amount": amount})

    def sell_all(self):
        stocks = self.ledger.get_stocks()
        for stock in stocks:
            if stocks[stock] > 0:
                self.sell(stock, stocks[stock])

    def reset(self):
        self.ledger = Ledger(self.initial_balance, self.tradable_stocks)
        self.current_date = self.start_date
        self.iterator = 0
        self.logs = []

    def store_result(self):
        self.results.append({"profit": self.ledger.balance - self.initial_balance,
                             "profit_percentage": ((self.ledger.balance - self.initial_balance)
                                                   / self.initial_balance) * 100,
                             "profit_percentage_year": profit_percentage_by_year(self.initial_balance,
                                                                                 self.ledger.balance,
                                                                                 time_between_days(self.start_date,
                                                                                                   self.end_date)),
                             "logs": self.logs})
        self.reset()

    def get_daily_data(self):
        daily_data = {}
        for ticker in self.tradable_stocks:
            daily_data[ticker] = self.data[ticker][self.iterator]
        return daily_data

    def get_current_stock_price(self, stock_name):
        return float(self.prices[stock_name][self.iterator])

    def get_data_by_ticker(self, ticker):
        return self.data[ticker]

    def get_prices(self, ticker):
        return self.prices[ticker]

    def get_current_value(self):
        cash = self.ledger.get_balance()
        stocks_value = 0
        stocks = self.ledger.get_stocks()
        for stock in stocks:
            stocks_value += self.get_current_stock_price(stock) * stocks[stock]
        return cash + stocks_value

    def get_results(self):
        return self.results

    def get_result(self, no_execution=0):
        if len(self.results) > no_execution:
            return self.results[no_execution]

    def get_ledger(self):
        return self.ledger

    def get_iteration(self):
        return self.iterator

    def get_initial_balance(self):
        return self.initial_balance

    def get_tradable_stocks(self):
        return self.tradable_stocks

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_model(self):
        return self.model

    def get_graph(self, mode="daily"):
        plt.xlabel("Time ({})".format(mode))
        plt.ylabel("Capital")
        y = []
        for el in self.get_evaluations(mode=mode):
            y.append(sum(el[1]) / len(el[1]))
        x = range(1, len(y) + 1)
        plt.plot(x, y)
        plt.show()

    def get_evaluations(self, mode="daily"):
        if mode == "daily":
            return self.evaluations
        elif mode == "monthly":
            filtered_evaluations = [self.evaluations[0]]
            for i in range(len(self.evaluations)):
                date = self.evaluations[i][0]
                previous_date = filtered_evaluations[-1][0]
                if get_year(date) != get_year(previous_date) or get_month(date) != get_month(previous_date):
                    filtered_evaluations.append(self.evaluations[i])
            return filtered_evaluations
        elif mode == "yearly":
            filtered_evaluations = [self.evaluations[0]]
            for i in range(len(self.evaluations)):
                date = self.evaluations[i][0]
                previous_date = filtered_evaluations[-1][0]
                if get_year(date) != get_year(previous_date):
                    filtered_evaluations.append(self.evaluations[i])
            return filtered_evaluations

    def logs_str(self, no_execution=0):
        if len(self.results) == 0:
            return
        logs = self.results[no_execution]["logs"]
        logs_format = ""
        for log in logs:
            logs_format += "\t{} {} stocks of {} with price {} at {}\n".format(log["action"], log["amount"],
                                                                               log["stock_name"],
                                                                               log["stock_price"],
                                                                               log["date"])
        return logs_format
