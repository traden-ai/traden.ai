from dataclasses import dataclass, field


@dataclass(frozen=True)
class EMA:
    """class for representing the EMA technical indicator"""

    ema20: float = field(default=None)
    ema50: float = field(default=None)
    ema100: float = field(default=None)
