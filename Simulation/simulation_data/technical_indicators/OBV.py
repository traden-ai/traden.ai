from dataclasses import dataclass, field


@dataclass
class OBV:
    """class for representing the OBV technical indicator"""

    obv: float = field(default=None)
