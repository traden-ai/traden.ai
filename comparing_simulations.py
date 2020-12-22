from models import *
from simulation import Simulation
import matplotlib.pyplot as plt

class ComparingSimulations:
    def __init__(self, list_of_simulations, executed=False):
        self.simulations = list_of_simulations
        self.executed = executed

    def execute(self, no_executions=1):
        for simul in self.simulations:
            simul.execute(no_executions)
        self.executed = True
 
    def get_simulations(self):
        return self.simulations

    def get_expected_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        return [sum(map(lambda x: float(x[metric]), simul.get_results())) / len(simul.get_results()) for simul in self.simulations]

    def get_best_simulation_by_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        expected_metric_values = self.get_expected_metric(metric=metric)
        return self.simulations[expected_metric_values.index(max(expected_metric_values))]

    def get_worst_simulation_by_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        expected_metric_values = self.get_expected_metric(metric=metric)
        return self.simulations[expected_metric_values.index(min(expected_metric_values))]
    
    def get_graph_comparison(self, mode="daily", label="id"):
        plt.xlabel("Time ({})".format(mode))
        plt.ylabel("Capital")    
        for simul in self.simulations:
            X = []
            Y = []
            for el in simul.get_evaluations(mode=mode):
                Y.append(sum(el[1]) / len(el[1]))
            X = range(1,len(Y) + 1)
            if label == "id":
                plt.plot(X,Y, label="{}".format(str(simul.get_id())))
            elif label == "model":
                plt.plot(X,Y, label="{}".format(simul.get_model()))
            elif label == "period":
                plt.plot(X,Y, label="{} -> {}".format(simul.get_start_date(), simul.get_end_date()))
            elif label == "stock":
                plt.plot(X,Y, label="{}".format(str(simul.get_tradable_stocks())))
        plt.legend(loc='best')
        plt.show()
