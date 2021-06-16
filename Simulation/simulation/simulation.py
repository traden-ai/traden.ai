from Simulation.ledger.ledger import Ledger
from Models.models.model_interface import ModelInterface, Action
from utils.utils import profit_percentage_by_year, time_between_days, get_year, get_month
from Simulation.simulation_data.daily_data import DailyData


class Simulation:

    def __init__(self, balance: float, tradable_stocks: list, model: ModelInterface, dates: list, data: dict,
                 prices: dict, no_executions: int):

        self.tradable_stocks = tradable_stocks
        self.ledger = Ledger(balance, tradable_stocks)
        self.model = model
        self.initial_balance = balance
        self.data = data
        self.dates = dates
        self.prices = prices
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

    def execute_day(self):
        daily_data = self.get_daily_data()
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
                self.execute_day()
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
        tradable_stocks = self.ledger.get_stocks()
        stocks_performance = {}
        for s in tradable_stocks:
            stocks_performance[s] = ((self.prices[s][-1] - self.prices[s][0])
                                     / self.prices[s][0]) * 100
        self.results.append({"profit": self.ledger.balance - self.initial_balance,
                             "profit_percentage": ((self.ledger.balance - self.initial_balance)
                                                   / self.initial_balance) * 100,
                             "profit_percentage_year": profit_percentage_by_year(self.initial_balance,
                                                                                 self.ledger.balance,
                                                                                 time_between_days(self.start_date,
                                                                                                   self.end_date)),
                             "operating_time_percentage": (self.operating_days / (self.iterator + 1)) * 100,
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
                                sum(self.results[0]["stocks_performance"].values()) / len(tradable_stocks)}

    def get_daily_data(self):
        daily_data = {}
        for ticker in self.tradable_stocks:
            daily_data[ticker] = DailyData(self.data[ticker][self.iterator])
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

    def get_avg_results(self):
        return self.avg_results

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

    def get_no_executions(self):
        return self.no_executions

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

    # FIXME not useful anymore (deletable)
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
