from dataclasses import dataclass, field


@dataclass(frozen=True)
class ADX:
    """class for representing the ADX technical indicator"""

    adx: float = field(default=None)
