
class EndpointInterface:

    name = "name for specific exchange"
    description = "default description for exchange"

    def __init__(self, name, description) -> None:
        name = name
        description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def buy(self):
        pass

    def sell(self):
        pass

    def get_current_prince(self, tickers: list):
        pass
