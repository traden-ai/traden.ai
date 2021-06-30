from dataclasses import dataclass, field


@dataclass(frozen=True)
class IncomeStatement:
    """class for representing fundamental data regarding income_statement"""

    fiscalDateEnding: str = field(default=None)
    reportedCurrency: str = field(default=None)
    grossProfit: float = field(default=None)
    totalRevenue: float = field(default=None)
    costOfRevenue: float = field(default=None)
    costOfGoodsAndServicesSold: float = field(default=None)
    operatingIncome: float = field(default=None)
    sellingGeneralAndAdministrative: float = field(default=None)
    researchAndDevelopment: float = field(default=None)
    operatingExpenses: float = field(default=None)
    investmentIncomeNet: float = field(default=None)
    netInterestIncome: float = field(default=None)
    interestIncome: float = field(default=None)
    interestExpense: float = field(default=None)
    nonInterestIncome: float = field(default=None)
    otherNonOperatingIncome: float = field(default=None)
    depreciation: float = field(default=None)
    depreciationAndAmortization: float = field(default=None)
    incomeBeforeTax: float = field(default=None)
    incomeTaxExpense: float = field(default=None)
    interestAndDebtExpense: float = field(default=None)
    netIncomeFromContinuingOperations: float = field(default=None)
    comprehensiveIncomeNetOfTax: float = field(default=None)
    ebit: float = field(default=None)
    ebitda: float = field(default=None)
    netIncome: float = field(default=None)
