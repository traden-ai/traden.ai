from Models.models.model_interface import ModelInterface


class UnivariateModel(ModelInterface):

    description = "default description for Univariate Model"

    ticker = None

    model = None

    def __init__(self, ticker, model):
        self.ticker = ticker
        self.model = model

    def execute(self, daily_data: dict) -> list:
        return self.model.execute({self.ticker : daily_data[self.ticker]})