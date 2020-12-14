from simulation import Simulation

class ComparingSimulations:
    def __init__(self, list_of_simulations, executed=False):
        self.simulations = list_of_simulations
        self.executed = executed

    def execute(self, no_executions=1):
        for simul in self.simulations:
            simul.execute(no_executions)
        self.executed = True
 
    def get_expected_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        return [sum(map(lambda x: float(x[metric]), simul.get_results())) / len(simul.get_results()) for simul in self.simulations]

    def get_best_simulation_by_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        expected_metric_values = self.get_expected_metric(metric=metric)
        return self.simulations[expected_metric_values.index(max(expected_metric_values))]


def buyAll(simulation):
    simulation.buy("AMZN", 1)
    

def buyRandom(simulation):
    from random import randint
    if randint(0,1):
        simulation.buy("AMZN", 1)
    else:
        simulation.sell("AMZN", 1)

def void(simulation):
    return None


if __name__=="__main__":
    simul1 = Simulation(4000,["AMZN"],"2020-01-01","2020-10-01",buyAll,void)
    simul2 = Simulation(4000,["AMZN"],"2020-01-01","2020-10-01",buyRandom,void)
    comp = ComparingSimulations([simul1,simul2])
    comp.execute(no_executions=1)
    print(comp.get_expected_metric(metric="profit_percentage"))
    print(comp.get_best_simulation_by_metric(metric="profit").get_results())

    
