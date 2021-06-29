from dataclasses import dataclass, field
from Simulation.simulation_data.technical_indicators import TechnicalIndicators
from Simulation.simulation_data.earnings import Earnings
from Simulation.simulation_data.balance_sheet import BalanceSheet
from Simulation.simulation_data.cash_flow import CashFlow
from Simulation.simulation_data.income_statement import IncomeStatement


@dataclass(frozen=True)
class DayData:
    """class for representing data pertaining to a specific day"""
    
    open: float = field(default=None)
    high: float = field(default=None)
    low: float = field(default=None)
    close: float = field(default=None)
    volume: float = field(default=None)

    earnings: Earnings = field(default=None)
    cash_flow: CashFlow = field(default=None)
    balance_sheet: BalanceSheet = field(default=None)
    income_statement: IncomeStatement = field(default=None)
    technical_indicators: TechnicalIndicators = field(default=None)
