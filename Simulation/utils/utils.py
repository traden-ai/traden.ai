from Simulation.simulation_data.SimulationData import SimulationData
from Simulation.simulation_data.stock_time_series.DailyAdjusted import DailyAdjusted
from Simulation.simulation_data.technical_indicators.EMA import EMA
from Simulation.simulation_data.technical_indicators.SMA import SMA
from Simulation.simulation_data.technical_indicators.MACD import MACD
from Simulation.simulation_data.technical_indicators.RSI import RSI
from Simulation.simulation_data.technical_indicators.VWAP import VWAP
from Simulation.simulation_data.technical_indicators.CCI import CCI
from Simulation.simulation_data.technical_indicators.ADX import ADX
from Simulation.simulation_data.technical_indicators.STOCH import STOCH
from Simulation.simulation_data.technical_indicators.AROON import AROON
from Simulation.simulation_data.technical_indicators.BBANDS import BBANDS
from Simulation.simulation_data.technical_indicators.AD import AD
from Simulation.simulation_data.technical_indicators.OBV import OBV
from Simulation.simulation_data.fundamental_data.CompanyOverview import CompanyOverview
from Simulation.simulation_data.fundamental_data.Earnings import Earnings
from Simulation.simulation_data.fundamental_data.BalanceSheet import BalanceSheet
from Simulation.simulation_data.fundamental_data.CashFlow import CashFlow
from Simulation.simulation_data.fundamental_data.IncomeStatement import IncomeStatement


def update_today_data(yesterday_data: dict, today_data: dict):
    """ This method updates the SimulationData dataclass instances from 'yesterday'
        with the provided data from 'today'
    """
    for ticker, data in today_data:
        aux_data = {}
        for indicator, components in data:
            aux_data[indicator] = SimulationDataClasses[indicator](**components)
        yesterday_data[ticker].__init__(**aux_data)

    return yesterday_data


def data_load(data_provider_data):
    """ This method processes the raw data provided by the data_provided
    and transforms it into clean data for a simulation execution
    """

    def daily_data_load(values):
        typed_data = {trading_data: {} for trading_data in SimulationDataClasses}

        for key, components in values:
            for component, value in components.components_to_values:
                typed_data[key][component] = type(getattr(SimulationDataClasses[key], component))(value)

        return typed_data

    dates = []
    data = {}
    prices = []

    for day_data in data_provider_data:
        dates.append(day_data.date)
        data[day_data.date] = {}
        prices.append({})
        for ticker_data in day_data.ticker_data:
            data[day_data.date][ticker_data.ticker] = daily_data_load(ticker_data.indicators_to_values)
            prices[-1][ticker_data.ticker] = float(ticker_data.indicators_to_values["dailyAdjusted"]
                                                   .components_to_values["adjustedClose"])

    return dates, data, prices


SimulationDataClasses = {
    "dailyAdjusted": DailyAdjusted, "sma": SMA, "ema": EMA, "macd": MACD, "rsi": RSI, "vwap": VWAP, "cci": CCI,
    "adx": ADX, "stoch": STOCH, "aroon": AROON, "bbands": BBANDS, "ad": AD, "obv": OBV,
    "companyOverview": CompanyOverview, "earnings": Earnings, "cashFlow": CashFlow, "incomeStatement": IncomeStatement,
    "balanceSheet": BalanceSheet
}
