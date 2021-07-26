from datetime import datetime
import matplotlib.pyplot as plt
import re
import os
from constants import PYTHON_PATH


def ask_balance():
    while True:
        try:
            balance = float(input("\n\tInitial balance: "))
            return balance
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_stocks():
    while True:
        stocks_raw = input("\n\tStock(s): ")
        stocks = re.split(", |,| ", stocks_raw.upper())
        return stocks


def ask_period():
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    while True:
        start_date = input("\n\tStart of the simulation: (YYYY-mm-dd) ")
        if not validate_date(start_date):
            print("\n\tPlease enter a valid date.")
            continue
        break
    while True:
        end_date = input("\n\tEnd of the simulation: (YYYY-mm-dd) ")
        if not validate_date(end_date):
            print("\n\tPlease enter a valid date.")
            continue
        return start_date, end_date


def ask_model_instances(instances):

    while True:
        model_instances_raw = input("\n\tModel instance(s): ")
        model_instances_clean = re.split(", |,| ", model_instances_raw)
        if model_instances_raw.lower() == "l":
            print("\n\t% Available Models Instances\n")
            if instances:
                for i, ins in enumerate(instances, start=1):
                    print("\t[" + str(i) + "]\t" + ins)
            else:
                print("\tSorry. No model instances available.")
            continue
        elif not all(item in instances or item.isdigit() and int(item) in range(1, len(instances) + 1)
                     for item in model_instances_clean):
            print("\n\tERROR: Invalid model instance(s).")
            print("\tPlease insert 'l' to consult the available instances.")
            continue

        return [i if not i.isdigit() else instances[int(i) - 1] for i in model_instances_clean]


def ask_executions():
    while True:
        try:
            no_exec = int(input("\n\tNumber of executions: "))
            return no_exec
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_simulation(instances: list):
    balance = ask_balance()
    stocks = ask_stocks()
    start_date, end_date = ask_period()
    model_instances = ask_model_instances(instances)
    no_exec = ask_executions()

    return balance, stocks, start_date, end_date, model_instances, no_exec


def ask_simulation_id():
    while True:
        try:
            id = int(input("\n\tSimulation ID: "))
            return id
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_graph():
    while True:
        option = input("\tPlot results into graph? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")


def render_graph(stream):
    plt.xlabel("Time (daily)")
    plt.ylabel("Capital")
    for model in stream:
        x = [el.time for el in stream[model]]
        y = [el.capital for el in stream[model]]
        plt.plot(x, y, label=f"{model}")
    plt.legend(loc='best')
    plt.show()


def ask_results():
    while True:
        option = input("\tStore simulation results? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")


def find_index(dir):
    files = os.listdir(dir)
    files = [f[0:f.find(".")] for f in files]
    return max(int(f) for f in files) + 1


def save_logs(sim_req, sim_results, logs):

    try:
        dir_path = PYTHON_PATH + "/App/app/simulation_history/"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        index = find_index(dir_path)
        filepath = dir_path + f"{index}.txt"

        with open(filepath, 'w') as f:
            f.write("+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Details" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(f"\n\tBalance {sim_req.balance}\n")
            f.write(f"\n\tStarting Date: {sim_req.interval.start_date}\n")
            f.write(f"\n\tEnding Date: {sim_req.interval.end_date}\n")
            f.write("\n\tModels used in the simulation:\n")
            [f.write(f"\t\t{model}\n") for model in sim_req.models]
            f.write("\n\tTickers used in the simulation:\n")
            [f.write(f"\t\t{ticker}\n") for ticker in sim_req.tickers]
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Results" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_simulation(sim_results))
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 32) + "Simulation Logs" + (" " * 31) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_logs(logs))
        return filepath

    except Exception as e:
        return "ERROR: Could not store the simulation data: " + str(e)


def render_logs(logs):

    ret = ""
    actions = {0: "Bought", 1: "Sold"}

    for ex in logs:
        logs_str = ""
        for l in logs[ex]:
            logs_str += "\t{} {} stocks of {} with price {} at {}\n".format(actions[l.action],
                l.amount, l.ticker, l.price_per_share, l.date)

        ret += "\nEx:\tRun {} of model {}\n".format(ex[1], ex[0])
        ret += logs_str
    
    return ret


def render_simulation(result):

    results_str = ""
    models = result.model_results
    tickers = result.ticker_results

    for m in models:
        results_str = "\n\tModel: {}".format(m.model)
        results_str += "\n\tEx:"
        results_str += "\tProfit: {}".format(m.nominal_profit)
        results_str += "\n\t\tProfit (%): {}".format(m.percentage_profit)
        results_str += "\n\t\tProfit (% / Year): {}".format(
            m.yearly_percentage_profit)
        results_str += "\n\t\tOperating time (%): {}\n".format(
            m.operating_time_percentage)
        
    for t in tickers:
        results_str += "\n\t\tProfit for {} stock (%): {}".format(
            t.ticker, t.percentage_profit)
 
    results_str += "\n\t\tAverage profit for chosen stocks (%): {}\n".format(sum(t.percentage_profit for t in tickers)/len(tickers))

    return results_str


