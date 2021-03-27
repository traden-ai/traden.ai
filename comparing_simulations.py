import matplotlib.pyplot as plt


class ComparingSimulations:
    def __init__(self, list_of_simulations, executed=False):
        self.simulations = list_of_simulations
        self.executed = executed

    def execute(self, no_executions=1):
        for sim in self.simulations:
            sim.execute(no_executions)
        self.executed = True

    def get_simulations(self):
        return self.simulations

    def get_expected_metric(self, metric="profit"):
        if not self.executed:
            self.execute()
        return [sum(map(lambda x: float(x[metric]), sim.get_results())) / len(sim.get_results()) for sim in
                self.simulations]

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
        for sim in self.simulations:
            y = []
            for el in sim.get_evaluations(mode=mode):
                y.append(sum(el[1]) / len(el[1]))
            x = range(1, len(y) + 1)
            if label == "id":
                plt.plot(x, y, label="{}".format(str(sim.get_id())))
            elif label == "model":
                plt.plot(x, y, label="{}".format(sim.get_model()))
            elif label == "period":
                plt.plot(x, y, label="{} -> {}".format(sim.get_start_date(), sim.get_end_date()))
            elif label == "stock":
                plt.plot(x, y, label="{}".format(str(sim.get_tradable_stocks())))
        plt.legend(loc='best')
        plt.show()
