class DailyData:
    """class for representing data pertaining to a specific day"""

    def __init__(self, data):
        self.open = float(data["daily"]["1. open"])
        self.high = float(data["daily"]["2. high"])
        self.low = float(data["daily"]["3. low"])
        self.close = float(data["daily"]["3. low"])
        self.volume = float(data["daily"]["5. volume"])

        self.sma = float(data["sma"]["SMA"])
        self.ema = float(data["ema"]["EMA"])

        self.macd = float(data["macd"]["MACD"])
        self.macd_hist = float(data["macd"]["MACD_Hist"])
        self.macd_signal = float(data["macd"]["MACD_Signal"])

        self.rsi = float(data["rsi"]["RSI"])
        self.cci = float(data["cci"]["CCI"])
        self.adx = float(data["adx"]["ADX"])

        self.stoch_slowd = float(data["stoch"]["SlowD"])
        self.stoch_slowk = float(data["stoch"]["SlowK"])

        self.aroon_up = float(data["aroon"]["Aroon Up"])
        self.aroon_down = float(data["aroon"]["Aroon Down"])

        self.bbands_real_upper = float(data["bbands"]["Real Upper Band"])
        self.bbands_real_middle = float(data["bbands"]["Real Middle Band"])
        self.bbands_real_lower = float(data["bbands"]["Real Lower Band"])

        self.ad = float(data["ad"]["Chaikin A/D"])
        self.obv = float(data["obv"]["OBV"])

        # TODO create specific classes
        self.earnings = None
        self.cash_flow = None
        self.income_statement = None
        self.balance_sheet = None

    # TODO create setters and and description
    # without this it still works since python has no such thing as private att
