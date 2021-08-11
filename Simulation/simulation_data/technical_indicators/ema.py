from dataclasses import dataclass, field


@dataclass
class EMA:
    """class for representing the EMA technical indicator"""

    ema20: float = field(default=.0)
    ema50: float = field(default=.0)
    ema100: float = field(default=.0)
