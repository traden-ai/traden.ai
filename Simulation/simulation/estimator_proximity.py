from models.estimator_interface import EstimatorInterface
from models.model_interface import ModelInterface
from simulation.simulation import Simulation
from utils.utils import vector_proj_of_vec1_on_vec2, \
    convert_dict_if_equal_keys_to_array


class EstimatorProximity:
    def __init__(self, estimatorModel1: EstimatorInterface, estimatorModel2: EstimatorInterface, tradable_stocks: list, start_date: str, end_date: str):
        self.simulation1 = Simulation(0, tradable_stocks, start_date, end_date, estimatorModel1)
        self.simulation2 = Simulation(0, tradable_stocks, start_date, end_date, estimatorModel2)
        self.simulation1.execute()
        self.simulation2.execute()

    def get_orthogonal_proximity(self):
        results1 = self.simulation1.get_results()
        results2 = self.simulation2.get_results()
        size1 = len(results1)
        size2 = len(results2)
        proximity = []
        if size1 == size2:
            for i in range(size1):
                data_point1 = results1[i]
                data_point2 = results2[i]
                if len(data_point1) == len(data_point2):
                    vec1, vec2 = convert_dict_if_equal_keys_to_array(data_point1, data_point2)
                    proximity.append(vector_proj_of_vec1_on_vec2(vec1, vec2))
        return proximity
