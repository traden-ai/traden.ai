from dataclasses import dataclass, field


@dataclass
class AROON:
    """class for representing the AROON technical indicator"""

    aroonUp: float = field(default=.0)
    aroonDown: float = field(default=.0)
