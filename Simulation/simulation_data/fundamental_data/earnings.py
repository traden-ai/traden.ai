from dataclasses import dataclass, field


@dataclass
class Earnings:
    """class for representing fundamental data regarding earnings"""

    fiscalDateEnding: str = field(default="")
    reportedDate: str = field(default="")
    reportedEPS: float = field(default=.0)
    estimatedEPS: float = field(default=.0)
    surprise: float = field(default=.0)
    surprisePercentage: float = field(default=.0)
