import threading

from Simulation.simulation.simulation import Simulation


class SimulationAssembler:

    def __init__(self, balance: float, tradable_tickers: list, model_instances: list, dates: list, daily_data: dict,
                 prices: list, transaction_fee: float, no_executions: int):

        self.tradable_tickers = tradable_tickers

        self.simulations = []
        for instance in model_instances:
            self.simulations.append(Simulation(balance, tradable_tickers, instance, dates, daily_data, prices,
                                               transaction_fee, no_executions))
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
        return [sum(map(lambda x: float(x[metric]), sim.results)) / len(sim.results)
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
                      key=lambda sim: sum(map(lambda x: float(x[metric]), sim.results)) / len(sim.results),
                      reverse=True)

    def get_graph(self, no_simulation, mode="daily"):
        x = 0
        graph = []
        sim = self.simulations[no_simulation]
        evaluations = sim.get_evaluations(mode=mode)
        for _, ev in evaluations:
            graph.append((x, sum(ev) / len(ev)))
            x = x + 1
        return graph

    def get_logs(self, no_simulation: int, no_execution: int):
        return self.simulations[no_simulation].results[no_execution]["logs"]
