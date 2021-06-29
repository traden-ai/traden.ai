from dataclasses import dataclass, field


@dataclass(frozen=True)
class TechnicalIndicators:
    """class for representing data regarding technical indicators"""

    ema: float = field(default=None)
    sma: float = field(default=None)
    macd: float = field(default=None)
    macd_hist: float = field(default=None)
    macd_signal: float = field(default=None)
    rsi: float = field(default=None)
    cci: float = field(default=None)
    adx: float = field(default=None)
    stoch_slowd: float = field(default=None)
    stoch_slowk: float = field(default=None)
    aroon_up: float = field(default=None)
    aroon_down: float = field(default=None)
    bbands_real_upper: float = field(default=None)
    bbands_real_middle: float = field(default=None)
    bbands_real_lower: float = field(default=None)
    ad: float = field(default=None)
    obv: float = field(default=None)
