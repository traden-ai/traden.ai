from Models.models.action import Action
from Simulation.ledger.ledger import Ledger
from Simulation.simulation_servicer.utils import *
from Models.models.model_interface import ModelInterface
from Simulation.simulation_data.simulation_data import SimulationData


class Simulation:

    def __init__(self, balance: float, tradable_tickers: list, model: ModelInterface, dates: list, daily_data: dict,
                 prices: list, transaction_fee: float, no_executions: int):

        self.tradable_tickers = tradable_tickers
        self.ledger = Ledger(balance, tradable_tickers)
        self.model = model
        self.initial_balance = balance
        self.daily_data = daily_data
        self.today_data = {ticker: SimulationData() for ticker in self.tradable_tickers}
        self.dates = dates
        self.prices = prices
        self.transaction_fee = transaction_fee
        self.no_executions = no_executions

        self.start_date = self.dates[0]
        self.current_date = self.start_date
        self.end_date = self.dates[-1]
        self.iterator = 0
        self.operating_days = 0

        self.logs = []
        self.results = []
        self.avg_results = {}
        self.evaluations = [(date, []) for date in self.dates]

    def buy(self, stock_name: str, amount: float):
        if amount > 0:
            stock_price = self.get_current_stock_price(stock_name)
            if self.ledger.buy(stock_name, stock_price, amount, self.transaction_fee):
                self.logs.append(
                    {
                        "action": Action.BUY,
                        "date": self.current_date,
                        "ticker": stock_name,
                        "price": stock_price,
                        "amount": amount
                    }
                )

    def sell(self, stock_name: str, amount: float):
        if amount > 0:
            stock_price = self.get_current_stock_price(stock_name)
            if self.ledger.sell(stock_name, stock_price, amount, self.transaction_fee):
                self.logs.append(
                    {
                        "action": Action.SELL,
                        "date": self.current_date,
                        "ticker": stock_name,
                        "price": stock_price,
                        "amount": amount
                    }
                )

    def sell_all(self):
        stocks = self.ledger.get_stocks()
        for stock in stocks:
            if stocks[stock] > 0:
                self.sell(stock, stocks[stock])

    def execute_day(self, daily_data):
        results = self.model.execute(daily_data)
        for result in results:
            if result["Action"] == Action.BUY:
                current_balance = self.ledger.get_balance()
                max_buy = current_balance // self.get_current_stock_price(result["Ticker"])
                self.buy(result["Ticker"], max_buy*result["Intensity"])
            elif result["Action"] == Action.SELL:
                max_sell = self.ledger.get_amount_stock(result["Ticker"])
                self.sell(result["Ticker"], max_sell*result["Intensity"])

    def execute(self):
        for i in range(self.no_executions):
            while self.current_date != self.end_date:
                self.today_data = update_today_data(self.today_data, self.daily_data[self.dates[self.iterator]])
                self.execute_day(self.today_data)
                if self.ledger.has_stocks():
                    self.operating_days += 1
                self.current_date = self.dates[self.iterator]
                self.evaluations[self.iterator][1].append(self.get_current_value())
                self.iterator += 1
            self.iterator -= 1
            self.current_date = self.dates[self.iterator]
            self.sell_all()
            self.store_result()
            self.reset()

    def reset(self):
        self.ledger = Ledger(self.initial_balance, self.tradable_tickers)
        self.current_date = self.start_date
        self.operating_days = 0
        self.iterator = 0
        self.logs = []

    def store_result(self):
        tradable_tickers = self.ledger.get_stocks()
        stocks_performance = {}
        for s in tradable_tickers:
            stocks_performance[s] = ((self.prices[-1][s] - self.prices[0][s])
                                     / self.prices[0][s]) * 100
        self.results.append({"profit": self.ledger.balance - self.initial_balance,
                             "profit_percentage": ((self.ledger.balance - self.initial_balance)
                                                   / self.initial_balance) * 100,
                             "profit_percentage_year": profit_percentage_by_year(self.initial_balance,
                                                                                 self.ledger.balance,
                                                                                 time_between_days(self.start_date,
                                                                                                   self.end_date)),
                             "operating_time_percentage": (self.operating_days / len(self.dates)) * 100,
                             "stocks_performance": stocks_performance,
                             "logs": self.logs})
        self.avg_results = {"profit": sum(map(lambda x: x["profit"], self.results)) / len(self.results),
                            "profit_percentage":
                                sum(map(lambda x: x["profit_percentage"], self.results)) / len(self.results),
                            "profit_percentage_year":
                                sum(map(lambda x: x["profit_percentage_year"], self.results)) / len(self.results),
                            "operating_time_percentage":
                                sum(map(lambda x: x["operating_time_percentage"], self.results)) / len(self.results),
                            "stocks_performance":
                                sum(self.results[0]["stocks_performance"].values()) / len(tradable_tickers)}

    def get_current_value(self):
        cash = self.ledger.get_balance()
        stocks_value = 0
        stocks = self.ledger.get_stocks()
        for stock in stocks:
            stocks_value += self.get_current_stock_price(stock) * stocks[stock]
        return cash + stocks_value

    def get_current_stock_price(self, stock_name):
        return float(self.prices[self.iterator][stock_name])

    def get_result(self, no_execution=0):
        if len(self.results) > no_execution:
            return self.results[no_execution]

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
