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

        return [i if not i.isdigit() else model_instances_clean[int(i) - 1] for i in instances]


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


def render_graph(stream):
    # FIXME daily? time seems to be predefined
    plt.xlabel("Time (daily)")
    plt.ylabel("Capital")
    for key, value in stream:
        x = [el.time for el in value.data_points]
        y = [el.capital for el in value.data_points]
        plt.plot(x, y, label=f"{key}")
    plt.legend(loc='best')
    plt.show()
