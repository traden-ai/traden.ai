from datetime import datetime
import matplotlib.pyplot as plt
import re


def ask_balance():
    while True:
        try:
            balance = float(input("\nInitial balance: "))
            return balance
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_stocks():
    while True:
        stocks_raw = input("\nStock(s): ")
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
        start_date = input("\nStart of the simulation: (YYYY-mm-dd) ")
        if not validate_date(start_date):
            print("\n\tPlease enter a valid date.")
            continue
        break
    while True:
        end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")
        if not validate_date(end_date):
            print("\n\tPlease enter a valid date.")
            continue
        return start_date, end_date


def ask_model_instances(instances):

    while True:
        model_instances_raw = input("\nModel instance(s): ")
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
            no_exec = int(input("\nNumber of executions: "))
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
            id = int(input("\nSimulation ID: "))
            return id
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_graph():
    while True:
        option = input("Plot results into graph? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")


def render_graph(stream):
    # FIXME daily? time seems to be predefined
    plt.xlabel("Time (daily)")
    plt.ylabel("Capital")
    for model in stream:
        x = [el.time for el in stream[model]]
        y = [el.capital for el in stream[model]]
        plt.plot(x, y, label=f"{model}")
    plt.legend(loc='best')
    plt.show()


def render_simulation(result):
    print(f"\n\t\tSimulation ID: {result.simulation_id}")

    models = result.model_results
    tickers = result.ticker_results

    for m in models:
        results_str = "\nEx:\t"
        results_str += "\tProfit: {}".format(m.nominal_profit)
        results_str += "\n\t\tProfit (% / Year): {}".format(
            m.percentage_profit)
        results_str += "\n\t\tOperating time (%): {}\n".format(
            m.operating_time_percentage)
        print(results_str)

    for t in tickers:
        print("\n\t\tProfit for {} stock (%): {}".format(
            t.ticker, t.percentage_profit))

    print("\n\t\tAverage profit for chosen stocks (%): {}\n".format(sum(t.percentage_profit for t in tickers)/len(tickers)))
