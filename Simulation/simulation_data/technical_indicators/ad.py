from dataclasses import dataclass, field


@dataclass
class AD:
    """class for representing the AD technical indicator"""

    ad: float = field(default=.0)
