from Models.models.model_interface import InputData

""" This file serves as a quickfix for some data issues that are still unresolved """

DatabaseNames2CorrectNames = {
    "1. open": "open",
    "2. high": "high",
    "3. low": "low",
    "4. close": "close",
    "5. volume": "volume",
    "operatingCashflow": "operatingCashFlow",
    "cashflowFromInvestment": "cashFlowFromInvestment",
    "cashflowFromFinancing": "cashFlowFromFinancing",
    "costofGoodsAndServicesSold": "costOfGoodsAndServicesSold",
    "otherNonCurrrentAssets": "otherNonCurrentAssets",
    "longTermDebtNoncurrent": "longTermDebtNonCurrent"
}

InputData2Keys = {
    InputData.PRICE_DATA: [
        "1. open",
        "2. high",
        "3. low",
        "4. close",
        "5. volume"
    ],
    InputData.TECHNICAL_INDICATORS: [
        "sma",
        "ema",
        "macd",
        "rsi",
        "cci",
        "adx",
        "stoch",
        "aroon",
        "bbands",
        "ad",
        "obv"
    ],
    InputData.EARNINGS: [
        "fiscalDateEnding",
        "reportedDate",
        "reportedEPS",
        "estimatedEPS",
        "surprise",
        "surprisePercentage"
    ],
    InputData.CASH_FLOW: [
        "fiscalDateEnding",
        "reportedCurrency",
        "operatingCashflow",
        "paymentsForOperatingActivities",
        "proceedsFromOperatingActivities",
        "changeInOperatingLiabilities",
        "changeInOperatingAssets",
        "depreciationDepletionAndAmortization",
        "capitalExpenditures",
        "changeInReceivables",
        "changeInInventory",
        "profitLoss",
        "cashflowFromInvestment",
        "cashflowFromFinancing",
        "proceedsFromRepaymentsOfShortTermDebt",
        "paymentsForRepurchaseOfCommonStock",
        "paymentsForRepurchaseOfEquity",
        "paymentsForRepurchaseOfPreferredStock",
        "dividendPayout",
        "dividendPayoutCommonStock",
        "dividendPayoutPreferredStock",
        "proceedsFromIssuanceOfCommonStock",
        "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
        "proceedsFromIssuanceOfPreferredStock",
        "proceedsFromRepurchaseOfEquity",
        "proceedsFromSaleOfTreasuryStock",
        "changeInCashAndCashEquivalents",
        "changeInExchangeRate",
        "netIncome"
    ],
    InputData.INCOME_STATEMENT: [
        "fiscalDateEnding",
        "reportedCurrency",
        "grossProfit",
        "totalRevenue",
        "costOfRevenue",
        "costofGoodsAndServicesSold",
        "operatingIncome",
        "sellingGeneralAndAdministrative",
        "researchAndDevelopment",
        "operatingExpenses",
        "investmentIncomeNet",
        "netInterestIncome",
        "interestIncome",
        "interestExpense",
        "nonInterestIncome",
        "otherNonOperatingIncome",
        "depreciation",
        "depreciationAndAmortization",
        "incomeBeforeTax",
        "incomeTaxExpense",
        "interestAndDebtExpense",
        "netIncomeFromContinuingOperations",
        "comprehensiveIncomeNetOfTax",
        "ebit",
        "ebitda",
        "netIncome"
    ],
    InputData.BALANCE_SHEET: [
        "fiscalDateEnding",
        "reportedCurrency",
        "totalAssets",
        "totalCurrentAssets",
        "cashAndCashEquivalentsAtCarryingValue",
        "cashAndShortTermInvestments",
        "inventory",
        "currentNetReceivables",
        "totalNonCurrentAssets",
        "propertyPlantEquipment",
        "accumulatedDepreciationAmortizationPPE",
        "intangibleAssets",
        "intangibleAssetsExcludingGoodwill",
        "goodwill",
        "investments",
        "longTermInvestments",
        "shortTermInvestments",
        "otherCurrentAssets",
        "otherNonCurrrentAssets",
        "totalLiabilities",
        "totalCurrentLiabilities",
        "currentAccountsPayable",
        "deferredRevenue",
        "currentDebt",
        "shortTermDebt",
        "totalNonCurrentLiabilities",
        "capitalLeaseObligations",
        "longTermDebt",
        "currentLongTermDebt",
        "longTermDebtNoncurrent",
        "shortLongTermDebtTotal",
        "otherCurrentLiabilities",
        "otherNonCurrentLiabilities",
        "totalShareholderEquity",
        "treasuryStock",
        "retainedEarnings",
        "commonStock",
        "commonStockSharesOutstanding"
    ]
}

Keys2InputData = {
    "1. open": {"type": float, "group": [InputData.PRICE_DATA]},
    "2. high": {"type": float, "group": [InputData.PRICE_DATA]},
    "3. low": {"type": float, "group": [InputData.PRICE_DATA]},
    "4. close": {"type": float, "group": [InputData.PRICE_DATA]},
    "5. volume": {"type": float, "group": [InputData.PRICE_DATA]},
    "sma": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "ema": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "macd": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "rsi": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "cci": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "adx": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "stoch": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "aroon": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "bbands": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "ad": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "obv": {"type": float, "group": [InputData.TECHNICAL_INDICATORS]},
    "fiscalDateEnding": {"type": str, "group": [InputData.EARNINGS, InputData.CASH_FLOW, InputData.INCOME_STATEMENT,
                                                InputData.BALANCE_SHEET]},
    "reportedDate": {"type": str, "group": [InputData.EARNINGS]},
    "reportedEPS": {"type": float, "group": [InputData.EARNINGS]},
    "estimatedEPS": {"type": float, "group": [InputData.EARNINGS]},
    "surprise": {"type": float, "group": [InputData.EARNINGS]},
    "surprisePercentage": {"type": float, "group": [InputData.EARNINGS]},
    "reportedCurrency": {"type": str, "group": [InputData.CASH_FLOW, InputData.INCOME_STATEMENT,
                                                InputData.BALANCE_SHEET]},
    "operatingCashflow": {"type": float, "group": [InputData.CASH_FLOW]},
    "paymentsForOperatingActivities": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromOperatingActivities": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInOperatingLiabilities": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInOperatingAssets": {"type": float, "group": [InputData.CASH_FLOW]},
    "depreciationDepletionAndAmortization": {"type": float, "group": [InputData.CASH_FLOW]},
    "capitalExpenditures": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInReceivables": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInInventory": {"type": float, "group": [InputData.CASH_FLOW]},
    "profitLoss": {"type": float, "group": [InputData.CASH_FLOW]},
    "cashflowFromInvestment": {"type": float, "group": [InputData.CASH_FLOW]},
    "cashflowFromFinancing": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromRepaymentsOfShortTermDebt": {"type": float, "group": [InputData.CASH_FLOW]},
    "paymentsForRepurchaseOfCommonStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "paymentsForRepurchaseOfEquity": {"type": float, "group": [InputData.CASH_FLOW]},
    "paymentsForRepurchaseOfPreferredStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "dividendPayout": {"type": float, "group": [InputData.CASH_FLOW]},
    "dividendPayoutCommonStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "dividendPayoutPreferredStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromIssuanceOfCommonStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromIssuanceOfPreferredStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromRepurchaseOfEquity": {"type": float, "group": [InputData.CASH_FLOW]},
    "proceedsFromSaleOfTreasuryStock": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInCashAndCashEquivalents": {"type": float, "group": [InputData.CASH_FLOW]},
    "changeInExchangeRate": {"type": float, "group": [InputData.CASH_FLOW]},
    "netIncome": {"type": float, "group": [InputData.CASH_FLOW, InputData.INCOME_STATEMENT]},
    "grossProfit": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "totalRevenue": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "costOfRevenue": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "costofGoodsAndServicesSold": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "operatingIncome": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "sellingGeneralAndAdministrative": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "researchAndDevelopment": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "operatingExpenses": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "investmentIncomeNet": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "netInterestIncome": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "interestIncome": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "interestExpense": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "nonInterestIncome": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "otherNonOperatingIncome": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "depreciation": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "depreciationAndAmortization": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "incomeBeforeTax": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "incomeTaxExpense": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "interestAndDebtExpense": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "netIncomeFromContinuingOperations": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "comprehensiveIncomeNetOfTax": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "ebit": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "ebitda": {"type": float, "group": [InputData.INCOME_STATEMENT]},
    "totalAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalCurrentAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "cashAndCashEquivalentsAtCarryingValue": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "cashAndShortTermInvestments": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "inventory": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "currentNetReceivables": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalNonCurrentAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "propertyPlantEquipment": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "accumulatedDepreciationAmortizationPPE": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "intangibleAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "intangibleAssetsExcludingGoodwill": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "goodwill": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "investments": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "longTermInvestments": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "shortTermInvestments": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "otherCurrentAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "otherNonCurrrentAssets": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalLiabilities": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalCurrentLiabilities": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "currentAccountsPayable": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "deferredRevenue": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "currentDebt": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "shortTermDebt": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalNonCurrentLiabilities": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "capitalLeaseObligations": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "longTermDebt": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "currentLongTermDebt": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "longTermDebtNoncurrent": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "shortLongTermDebtTotal": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "otherCurrentLiabilities": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "otherNonCurrentLiabilities": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "totalShareholderEquity": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "treasuryStock": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "retainedEarnings": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "commonStock": {"type": float, "group": [InputData.BALANCE_SHEET]},
    "commonStockSharesOutstanding": {"type": float, "group": [InputData.BALANCE_SHEET]}
}
