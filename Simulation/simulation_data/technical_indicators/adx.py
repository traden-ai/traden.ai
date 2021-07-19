from dataclasses import dataclass, field


@dataclass
class ADX:
    """class for representing the ADX technical indicator"""

    adx: float = field(default=.0)
