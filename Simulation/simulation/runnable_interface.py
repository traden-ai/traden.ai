from Simulation.ledger.ledger import Ledger
from Models.models.model_interface import ModelInterface, Action


# FIXME not useful anymore (deletable)
class Runnable:

    def __init__(self, balance: float, tradable_stocks: list, model: ModelInterface):
        self.tradable_stocks = tradable_stocks
        self.ledger = Ledger(balance, tradable_stocks)
        self.model = model

    def set_model(self, model: ModelInterface):
        """Sets a model in the respective runnable"""
        self.model = model

    def execute_day(self):
        """Executes a certain day in the respective runnable"""
        daily_data = self.get_daily_data()
        results = self.model.execute(daily_data)
        for result in results:
            if result["Action"] == Action.BUY:
                current_balance = self.ledger.get_balance()
                max_buy = current_balance // self.get_current_stock_price(result["Ticker"])
                self.buy(result["Ticker"], round(max_buy * result["Intensity"]))
            elif result["Action"] == Action.SELL:
                max_sell = self.ledger.get_amount_stock(result["Ticker"])
                self.sell(result["Ticker"], round(max_sell * result["Intensity"]))

    def get_current_stock_price(self, stock_name: str) -> float:
        """Gets the stock price for the corresponding stock_name"""
        pass

    def get_daily_data(self) -> dict:
        """Gets the respective data for a certain day in the respective runnable"""
        pass

    def buy(self, stock_name: str, amount: int) -> None:
        """Buys a certain amount of a certain stock"""
        pass

    def sell(self, stock_name: str, amount: int) -> None:
        """Sells a certain amount of a certain stock"""
        pass

    def sell_all(self):
        """Sells all stocks currently owned"""
        pass
