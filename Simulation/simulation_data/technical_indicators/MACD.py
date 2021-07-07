from dataclasses import dataclass, field


@dataclass
class MACD:
    """class for representing the MACD technical indicator"""

    macd: float = field(default=.0)
    macdHist: float = field(default=.0)
    macdSignal: float = field(default=.0)
