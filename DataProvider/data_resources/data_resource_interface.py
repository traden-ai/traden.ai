class DataResourceInterface:

    description = "default description for data resource"

    indicators_to_python_object = {} # For each indicator there is a function to retrieve string object into py object

    def get_description(self):
        return self.description

    def get_daily_data(self, tickers: list, indicators: list) -> list:
        """Data Resource should return respective data in the format
        {indicator: data in string format}
        """
        pass

    def get_past_data(self, tickers: list, indicators: list, init_date: str, end_date: str):
        """Data Resource should return past data in the format
        {ticker : {date: {indicator: data in string format, ...}, ...}, ...}
        """
        pass