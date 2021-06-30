from dataclasses import dataclass, field


@dataclass(frozen=True)
class DailyAdjusted:
    """class for representing daily price data"""

    open: float = field(default=None)
    high: float = field(default=None)
    low: float = field(default=None)
    close: float = field(default=None)
    adjustedClose: float = field(default=None)
    volume: float = field(default=None)
    dividendAmount: float = field(default=None)
    splitCoefficient: float = field(default=None)
