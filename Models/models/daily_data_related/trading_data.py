from enum import Enum


class TradingData(Enum):
    dailyAdjusted = 1
    sma = 2
    ema = 3
    macd = 4
    rsi = 5
    vwap = 6
    cci = 7
    adx = 8
    stoch = 9
    aroon = 10
    bbands = 11
    ad = 12
    obv = 13
    companyOverview = 14
    earnings = 15
    cashFlow = 16
    balanceSheet = 17
    incomeStatement = 18
