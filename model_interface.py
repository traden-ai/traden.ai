
class ModelInterface:
    def __init__(self, data: list) -> None:
        """ Creates the class instance"""
        pass
    
    def preprocess_data(self) -> None:
        """Does preprocessing associated with trading model"""
        pass
    
    def execute(self, simul) -> None:
        """Executes actions for a certain day in the respective Simulation"""
        pass