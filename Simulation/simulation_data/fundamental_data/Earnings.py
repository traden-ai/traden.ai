from dataclasses import dataclass, field


@dataclass(frozen=True)
class Earnings:
    """class for representing fundamental data regarding earnings"""

    fiscalDateEnding: str = field(default=None)
    reportedDate: str = field(default=None)
    reportedEPS: float = field(default=None)
    estimatedEPS: float = field(default=None)
    surprise: float = field(default=None)
    surprisePercentage: float = field(default=None)
