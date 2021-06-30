from dataclasses import dataclass, field


@dataclass(frozen=True)
class RSI:
    """class for representing the RSI technical indicator"""

    rsi: float = field(default=None)
