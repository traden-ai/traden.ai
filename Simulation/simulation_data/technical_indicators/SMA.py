from dataclasses import dataclass, field


@dataclass
class SMA:
    """class for representing the SMA technical indicator"""

    sma20: float = field(default=None)
    sma50: float = field(default=None)
    sma100: float = field(default=None)
