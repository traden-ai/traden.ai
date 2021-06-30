from dataclasses import dataclass, field


@dataclass(frozen=True)
class AD:
    """class for representing the AD technical indicator"""

    chaikinAD: float = field(default=None)
