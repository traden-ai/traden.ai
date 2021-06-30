from dataclasses import dataclass, field


@dataclass(frozen=True)
class VWAP:
    """class for representing the VWAP technical indicator"""

    vwap: float = field(default=None)
