from Models.models.model_interface import ModelInterface


class CompositionUnivariateModel(ModelInterface):
    description = "default description for Composition Univariate Model"

    tickers_with_models = {}

    capital_allocator = None

    def __init__(self, univariate_models: list, capital_allocator):
        for model in univariate_models:
            self.tickers_with_models[model.ticker] = model
        self.capital_allocator = capital_allocator(self.tickers_with_models)

    def execute(self, daily_data: dict) -> list:
        final_results = []
        for ticker in self.tickers_with_models:
            if ticker in daily_data:
                results = self.tickers_with_models[ticker].execute(daily_data)
                coef = self.capital_allocator.get_allocation(ticker)
                for result in results:
                    result["Intensity"] *= coef
                final_results.append(results)
        return final_results
