import threading
import matplotlib.pyplot as plt
from Simulation.simulation.simulation import Simulation


class SimulationAssembler:

    def __init__(self, balance: float, tradable_stocks: list, model_instances: list, historical_data: dict,
                 no_executions: int):

        # TODO parse data for simulations
        dates, data, prices = historical_data

        self.simulations = []
        for instance in model_instances:
            self.simulations.append(Simulation(balance, tradable_stocks, instance, dates, data, prices, no_executions))
        self.no_executions = no_executions
        self.executed = False

    def get_simulations(self):
        return self.simulations

    def execute(self):
        def execute_simulation(s: Simulation):
            s.execute()

        threads = [threading.Thread(target=execute_simulation, args=(sim,))
                   for sim in self.simulations]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.executed = True

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

    def get_graph(self, no_simulation, mode="daily"):
        # FIXME return data points instead of plotting graph
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

    def get_logs(self, no_simulation: int, no_execution: int):
        # TODO
        pass
