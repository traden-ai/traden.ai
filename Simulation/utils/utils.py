from Simulation.utils.data_translator import *
from Simulation.simulation_data.day_data import DayData
from Simulation.simulation_data.technical_indicators import TechnicalIndicators
from Simulation.simulation_data.earnings import Earnings
from Simulation.simulation_data.cash_flow import CashFlow
from Simulation.simulation_data.balance_sheet import BalanceSheet
from Simulation.simulation_data.income_statement import IncomeStatement


def data_load(data_provider_data, input_groups):
    """ This method processes the raw data provided by the data_provided
    and transforms it into clean data for a simulation execution
    """

    def daily_data_load(values):
        clean_data = {"technical_indicators": {}, "earnings": {}, "cash_flow": {}, "balance_sheet": {},
                      "income_statement": {}}

        for key, value in values:
            clean_key = DatabaseKeySpecification[key]["clean_name"]
            key_type = DatabaseKeySpecification[key]["type"]
            key_groups = set(set(DatabaseKeySpecification[key]["group"]) and input_groups)

            if InputData.PRICE_DATA in key_groups:
                clean_data[clean_key] = key_type(value)
            if InputData.TECHNICAL_INDICATORS in key_groups:
                clean_data["technical_indicators"][clean_key] = key_type(value)
            if InputData.EARNINGS in key_groups:
                clean_data["earnings"][clean_key] = key_type(value)
            if InputData.CASH_FLOW in key_groups:
                clean_data["cash_flow"][clean_key] = key_type(value)
            if InputData.BALANCE_SHEET in key_groups:
                clean_data["balance_sheet"][clean_key] = key_type(value)
            if InputData.INCOME_STATEMENT in key_groups:
                clean_data["income_statement"][clean_key] = key_type(value)

        for key in clean_data:
            if isinstance(clean_data[key], dict) and clean_data[key] != {}:
                if key == "technical_indicators":
                    clean_data[key] = TechnicalIndicators(**clean_data[key])
                elif key == "earnings":
                    clean_data[key] = Earnings(**clean_data[key])
                elif key == "cash_flow":
                    clean_data[key] = CashFlow(**clean_data[key])
                elif key == "balance_sheet":
                    clean_data[key] = BalanceSheet(**clean_data[key])
                elif key == "income_statement":
                    clean_data[key] = IncomeStatement(**clean_data[key])

        return DayData(**clean_data)

    dates = []
    data = {}
    prices = []

    for day_data in data_provider_data:
        dates.append(day_data.date)
        data[day_data.date] = {}
        prices.append({})
        for ticker_data in day_data.ticker_data:
            data[day_data.date][ticker_data.ticker] = daily_data_load(ticker_data.indicators_to_values)
            prices[-1][ticker_data.ticker] = float(ticker_data.indicators_to_values["1. close"])

    return dates, data, prices
