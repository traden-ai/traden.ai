from dataclasses import dataclass, field


@dataclass
class CashFlow:
    """class for representing fundamental data regarding cash flows"""

    fiscalDateEnding: str = field(default="")
    reportedCurrency: str = field(default="")
    operatingCashFlow: float = field(default=.0)
    paymentsForOperatingActivities: float = field(default=.0)
    proceedsFromOperatingActivities: float = field(default=.0)
    changeInOperatingLiabilities: float = field(default=.0)
    changeInOperatingAssets: float = field(default=.0)
    depreciationDepletionAndAmortization: float = field(default=.0)
    capitalExpenditures: float = field(default=.0)
    changeInReceivables: float = field(default=.0)
    changeInInventory: float = field(default=.0)
    profitLoss: float = field(default=.0)
    cashFlowFromInvestment: float = field(default=.0)
    cashFlowFromFinancing: float = field(default=.0)
    proceedsFromRepaymentsOfShortTermDebt: float = field(default=.0)
    paymentsForRepurchaseOfCommonStock: float = field(default=.0)
    paymentsForRepurchaseOfEquity: float = field(default=.0)
    paymentsForRepurchaseOfPreferredStock: float = field(default=.0)
    dividendPayout: float = field(default=.0)
    dividendPayoutCommonStock: float = field(default=.0)
    dividendPayoutPreferredStock: float = field(default=.0)
    proceedsFromIssuanceOfCommonStock: float = field(default=.0)
    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet: float = field(default=.0)
    proceedsFromIssuanceOfPreferredStock: float = field(default=.0)
    proceedsFromRepurchaseOfEquity: float = field(default=.0)
    proceedsFromSaleOfTreasuryStock: float = field(default=.0)
    changeInCashAndCashEquivalents: float = field(default=.0)
    changeInExchangeRate: float = field(default=.0)
    netIncome: float = field(default=.0)
