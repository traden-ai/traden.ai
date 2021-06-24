from DataProvider.data_resources.data_resource_interface import DataResourceInterface
from DataProvider.data_resources.resource_handler.utils import intersection, unite_raw_data
from DataProvider.data_resources.resources.alpha_vantage_resource import AlphaVantage
from DataProvider.database_handler.database_handler import DatabaseHandler


class ResourceHandler(DataResourceInterface):
    name = "ResourceHandler"

    description = "Handler responsible for aggregating multiple data resources"

    data_resources = None
    db_handler = None
    indicators_by_resource_name = {}

    def __init__(self, data_resources: list, db_handler):
        self.data_resources = data_resources
        self.db_handler = db_handler
        self.reset_indicators()

    def reset_indicators(self):
        for resource in self.data_resources:
            indicators = self.db_handler.get_indicators(resourceIdentifier=resource.name)
            for indicator in indicators:
                if resource.name in self.indicators_by_resource_name:
                    self.indicators_by_resource_name[resource.name].append(indicator)
                else:
                    self.indicators_by_resource_name[resource.name] = [indicator]

    def get_past_data(self, tickers: list, indicators: list, start_date: str, end_date: str):
        """Data Resource should return past data in the format
        {ticker : {date: {indicator: data in string format, ...}, ...}, ...}
        """
        raw_data = []
        for resource in self.data_resources:
            intersec_indicators = intersection(self.indicators_by_resource_name[resource.name], indicators)
            raw_data.append(resource.get_past_data(tickers, intersec_indicators, start_date, end_date))
        data = unite_raw_data(raw_data)
        return data


if __name__ == "__main__":
    res = ResourceHandler([AlphaVantage()], DatabaseHandler())
