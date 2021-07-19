from dataclasses import dataclass, field
from Simulation.simulation_data.stock_time_series.daily_adjusted import DailyAdjusted
from Simulation.simulation_data.technical_indicators.ema import EMA
from Simulation.simulation_data.technical_indicators.sma import SMA
from Simulation.simulation_data.technical_indicators.macd import MACD
from Simulation.simulation_data.technical_indicators.rsi import RSI
from Simulation.simulation_data.technical_indicators.vwap import VWAP
from Simulation.simulation_data.technical_indicators.cci import CCI
from Simulation.simulation_data.technical_indicators.adx import ADX
from Simulation.simulation_data.technical_indicators.stoch import STOCH
from Simulation.simulation_data.technical_indicators.aroon import AROON
from Simulation.simulation_data.technical_indicators.bbands import BBANDS
from Simulation.simulation_data.technical_indicators.ad import AD
from Simulation.simulation_data.technical_indicators.obv import OBV
from Simulation.simulation_data.fundamental_data.company_overview import CompanyOverview
from Simulation.simulation_data.fundamental_data.earnings import Earnings
from Simulation.simulation_data.fundamental_data.cash_flow import CashFlow
from Simulation.simulation_data.fundamental_data.income_statement import IncomeStatement
from Simulation.simulation_data.fundamental_data.balance_sheet import BalanceSheet


@dataclass(frozen=True)
class SimulationData:
    """class for representing data pertaining to a specific day"""

    dailyAdjusted: DailyAdjusted = field(default=None)
    sma: SMA = field(default=None)
    ema: EMA = field(default=None)
    macd: MACD = field(default=None)
    rsi: RSI = field(default=None)
    vwap: VWAP = field(default=None)
    cci: CCI = field(default=None)
    adx: ADX = field(default=None)
    stoch: STOCH = field(default=None)
    aroon: AROON = field(default=None)
    bbands: BBANDS = field(default=None)
    ad: AD = field(default=None)
    obv: OBV = field(default=None)
    companyOverview: CompanyOverview = field(default=None)
    earnings: Earnings = field(default=None)
    cashFlow: CashFlow = field(default=None)
    incomeStatement: IncomeStatement = field(default=None)
    balanceSheet: BalanceSheet = field(default=None)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
