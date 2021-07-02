from dataclasses import dataclass, field


@dataclass
class CCI:
    """class for representing the CCI technical indicator"""

    cci: float = field(default=None)
