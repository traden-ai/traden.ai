from dataclasses import dataclass, field


@dataclass
class MACD:
    """class for representing the MACD technical indicator"""

    macd: float = field(default=None)
    macdHist: float = field(default=None)
    macdSignal: float = field(default=None)
