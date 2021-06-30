def retry_if_value_error(exception):
    return isinstance(exception, ValueError)


def transform_key_to(data, oldToNewName):
    new_data = {}
    for date in data:
        new_data[date] = {}
        for name in data[date]:
            if name in oldToNewName:
                new_data[date][oldToNewName[name]] = data[date][name]
            else:
                new_data[date][name] = data[date][name]
    return new_data

def unite_data(data1, data2):
    for date in data2:
        data1[date].update(data2[date])
    return data1

dailyAdjustedOld2NewNames = {
    "1. open": "open",
    "2. high": "high",
    "3. low": "low",
    "4. close": " close",
    "5. adjusted close": "adjustedClose",
    "6. volume": "volume",
    "7. dividend amount": "dividendAmount",
    "8. split coefficient": "splitCoefficient"
}

smaOld2NewNames = {
    "SMA": "sma"
}

emaOld2NewNames = {
    "EMA": "ema"
}

macdOld2NewNames = {
    "MACD": "macd",
    "MACD_Hist": "macdHist",
    "MACD_Signal": "macdSignal"
}

rsiOld2NewNames = {
    "RSI": "rsi"
}

vwapOld2NewNames = {
    "VWAP": "vwap"
}

cciOld2NewNames = {
    "CCI": "cci"
}

stochOld2NewNames = {
    "SlowK": "slowK",
    "SlowD": "slowD"
}

adxOld2NewNames = {
    "ADX": "adx"
}

aroonOld2NewNames = {
    "Aroon Up": "aroonUp",
    "Aroon Down": "aroonDown"
}

bbandsOld2NewNames = {
    "Real Upper Band": "realUpperBand",
    "Real Middle Band": "realMiddleBand",
    "Real Lower Band": "realLowerBand"
}

adOld2NewNames = {
    "Chaikin A/D": "ad"
}

obvOld2NewNames = {
    "OBV": "obv"
}

companyOverviewOld2NewNames = {
    "Symbol": "symbol",
    "AssetType": "assetType",
    "Name": "name",
    "CIK": "cik",
    "Exchange": "exchange",
    "Currency": "currency",
    "Country": "country",
    "Sector": "sector",
    "Industry": "industry",
    "Address": "address",
    "FiscalYearEnd": "fiscalYearEnd",
    "LatestQuarter": "latestQuarter",
    "MarketCapitalization": "marketCapitalization",
    "EBITDA": "ebitda",
    "PERatio": "peRatio",
    "PEGRatio": "pegRatio",
    "BookValue": "bookValue",
    "DividendPerShare": "dividendPerShare",
    "DividendYield": "dividendYield",
    "EPS": "eps",
    "RevenuePerShareTTM": "revenuePerShareTTM",
    "ProfitMargin": "profitMargin",
    "OperatingMarginTTM": "operatingMarginTTM",
    "ReturnOnAssetsTTM": "returnOnAssetsTTM",
    "ReturnOnEquityTTM": "returnOnEquityTTM",
    "RevenueTTM": "revenueTTM",
    "GrossProfitTTM": "grossProfitTTM",
    "DilutedEPSTTM": "dilutedEPSTTM",
    "QuarterlyEarningsGrowthYOY": "quarterlyEarningsGrowthYOY",
    "QuarterlyRevenueGrowthYOY": "quarterlyRevenueGrowthYOY",
    "AnalystTargetPrice": "analystTargetPrice",
    "TrailingPE": "trailingPE",
    "ForwardPE": "forwardPE",
    "PriceToSalesRatioTTM": "priceToSalesRatioTTM",
    "PriceToBookRatio": "priceToBookRatio",
    "EVToRevenue": "evToRevenue",
    "EVToEBITDA": "evToEBITDA",
    "Beta": "beta",
    "52WeekHigh": "weekHigh52",
    "52WeekLow": "weekLow52",
    "50DayMovingAverage": "dayMovingAverage50",
    "200DayMovingAverage": "dayMovingAverage200",
    "SharesOutstanding": "sharesOutstanding",
    "SharesFloat": "sharesFloat",
    "SharesShort": "sharesShort",
    "SharesShortPriorMonth": "sharesShortPriorMonth",
    "ShortRatio": "shortRatio",
    "ShortPercentOutstanding": "shortPercentOutstanding",
    "ShortPercentFloat": "shortPercentFloat",
    "PercentInsiders": "percentInsiders",
    "PercentInstitutions": "percentInstitutions",
    "ForwardAnnualDividendRate": "forwardAnnualDividendRate",
    "ForwardAnnualDividendYield": "forwardAnnualDividendYield",
    "PayoutRatio": "payoutRatio",
    "DividendDate": "dividendDate",
    "ExDividendDate": "exDividendDate",
    "LastSplitFactor": "lastSplitFactor",
    "LastSplitDate": "lastSplitDate"
}

earningsOld2NewNames = {
    "operatingCashflow": "operatingCashFlow",
    "cashflowFromInvestment": "cashFlowFromInvestment",
    "cashflowFromFinancing": "cashFlowFromFinancing"
}

cashFlowOld2NewNames = {
    # empty
}

incomeStatementOld2NewNames = {
    "costofGoodsAndServicesSold": "costOfGoodsAndServicesSold"
}

balanceSheetOld2NewNames = {
    "otherNonCurrrentAssets": "otherNonCurrentAssets",
    "longTermDebtNoncurrent": "longTermDebtNonCurrent"
}
