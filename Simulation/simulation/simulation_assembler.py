import threading
import matplotlib.pyplot as plt
from simulation.simulation import Simulation
from utils.utils import data_load


class SimulationAssembler:

    def __init__(self, balance: float, tradable_stocks: list, start_date: str, end_date: str, model_instances: list):

        dates, data, prices = data_load(tradable_stocks, start_date, end_date)

        self.simulations = []
        for instance in model_instances:
            self.simulations.append(Simulation(balance, tradable_stocks, instance, dates, data, prices))

        self.executed = False

    def execute(self, no_executions=1):
        def execute_simulation(s: Simulation, no_exec: int):
            s.execute(no_exec)

        threads = [threading.Thread(target=execute_simulation, args=(sim, no_executions))
                   for sim in self.simulations]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.executed = True

    def get_simulations(self):
        return self.simulations

    def get_expected_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        return [sum(map(lambda x: float(x[metric]), sim.get_results())) / len(sim.get_results())
                for sim in self.simulations]

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

    def get_ordered_simulations(self, metric="profit"):
        if not self.executed:
            self.execute()
        return sorted(self.simulations,
                      key=lambda sim: sum(map(lambda x: float(x[metric]), sim.get_results())) / len(sim.get_results()),
                      reverse=True)

    def get_graph_comparison(self, mode="daily"):
        plt.xlabel("Time ({})".format(mode))
        plt.ylabel("Capital")
        for sim in self.simulations:
            y = []
            for el in sim.get_evaluations(mode=mode):
                y.append(sum(el[1]) / len(el[1]))
            x = range(1, len(y) + 1)
            plt.plot(x, y, label="{}".format(sim.get_model().__class__.__name__))
        plt.legend(loc='best')
        plt.show()
