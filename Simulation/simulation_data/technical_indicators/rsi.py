from dataclasses import dataclass, field


@dataclass
class RSI:
    """class for representing the RSI technical indicator"""

    rsi: float = field(default=.0)
