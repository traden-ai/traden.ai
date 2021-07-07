from dataclasses import dataclass, field


@dataclass
class STOCH:
    """class for representing the STOCH technical indicator"""

    slowK: float = field(default=.0)
    slowD: float = field(default=.0)
