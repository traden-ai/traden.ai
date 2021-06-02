from uno import Enum

from models.model_interface import ModelInterface
from utils.utils import filter_by_ticket, majority_voting


class EnsembleInterface(ModelInterface):
    models = []

    decider = None

    def __init__(self, models: list, decider):
        self.models = models
        self.decider = decider

    def execute(self, daily_data: dict) -> list:
        results = []
        for model in self.models:
            results.append(model.execute(daily_data))
        return self.decider(results)

    def save_attributes(self):
        for model in self.models:
            model.save_attributes()

    def retrieve_attributes(self):
        for model in self.models:
            model.retrieve_attributes()


if __name__ == "__main__":
    from model_database_handler.model_database_handler import get_instance, save_instance

    model1 = get_instance("NeuralNetEstimator")
    model2 = get_instance("NeuralNet")
    ensemble = EnsembleInterface([model1, model2], majority_voting)
    save_instance("FirstEnsemble", ensemble)
