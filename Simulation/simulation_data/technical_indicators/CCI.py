from dataclasses import dataclass, field


@dataclass(frozen=True)
class CCI:
    """class for representing the CCI technical indicator"""

    cci: float = field(default=None)
