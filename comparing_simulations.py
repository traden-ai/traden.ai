from simulation import Simulation

class ComparingSimulations:
    def __init__(self, list_of_simulations, no_executions, executed=False):
        self.simulations = list_of_simulations
        self.no_executions = no_executions
        self.executed = executed

    def execute():
        for simul in self.simulations:
            simul.execute(self.no_executions)
        self.executed = True

    def get_expected_metric(metric="profit"):
        if not self.executed:
            self.execute()
        return [sum(simul.get_results(),lambda x: float(x[metric])) / len(simul.get_results()) for simul in self.simulations]

    def get_best_simulation_by_metric(metric="profit"):
        expected_metric_values = self.get_expected_metric(**kwargs)
        return self.simulations[expected_metric_values.index(max(expected_metric_values))]



    
