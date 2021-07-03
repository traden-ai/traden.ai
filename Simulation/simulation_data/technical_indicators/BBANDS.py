from dataclasses import dataclass, field


@dataclass
class BBANDS:
    """class for representing the BBANDS technical indicator"""

    realUpperBand: float = field(default=None)
    realMiddleBand: float = field(default=None)
    realLowerBand: float = field(default=None)
