from dataclasses import dataclass, field
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
    balanceSheet: BalanceSheet = field(default=None)
    incomeStatement: IncomeStatement = field(default=None)
