from dataclasses import dataclass, field


@dataclass
class BBANDS:
    """class for representing the BBANDS technical indicator"""

    realUpperBand: float = field(default=.0)
    realMiddleBand: float = field(default=.0)
    realLowerBand: float = field(default=.0)
