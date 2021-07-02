from dataclasses import dataclass, field


@dataclass
class AROON:
    """class for representing the AROON technical indicator"""

    aroonUp: float = field(default=None)
    aroonDown: float = field(default=None)
