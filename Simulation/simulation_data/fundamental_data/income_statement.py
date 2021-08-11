from dataclasses import dataclass, field


@dataclass
class IncomeStatement:
    """class for representing fundamental data regarding income_statement"""

    fiscalDateEnding: str = field(default="")
    reportedCurrency: str = field(default="")
    grossProfit: float = field(default=.0)
    totalRevenue: float = field(default=.0)
    costOfRevenue: float = field(default=.0)
    costOfGoodsAndServicesSold: float = field(default=.0)
    operatingIncome: float = field(default=.0)
    sellingGeneralAndAdministrative: float = field(default=.0)
    researchAndDevelopment: float = field(default=.0)
    operatingExpenses: float = field(default=.0)
    investmentIncomeNet: float = field(default=.0)
    netInterestIncome: float = field(default=.0)
    interestIncome: float = field(default=.0)
    interestExpense: float = field(default=.0)
    nonInterestIncome: float = field(default=.0)
    otherNonOperatingIncome: float = field(default=.0)
    depreciation: float = field(default=.0)
    depreciationAndAmortization: float = field(default=.0)
    incomeBeforeTax: float = field(default=.0)
    incomeTaxExpense: float = field(default=.0)
    interestAndDebtExpense: float = field(default=.0)
    netIncomeFromContinuingOperations: float = field(default=.0)
    comprehensiveIncomeNetOfTax: float = field(default=.0)
    ebit: float = field(default=.0)
    ebitda: float = field(default=.0)
    netIncome: float = field(default=.0)
