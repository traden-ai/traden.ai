from dataclasses import dataclass, field


@dataclass
class DailyAdjusted:
    """class for representing daily price data"""

    open: float = field(default=.0)
    high: float = field(default=.0)
    low: float = field(default=.0)
    close: float = field(default=.0)
    adjustedClose: float = field(default=.0)
    volume: float = field(default=.0)
    dividendAmount: float = field(default=.0)
    splitCoefficient: float = field(default=.0)
