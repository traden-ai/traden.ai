import re
from datetime import datetime
from simulation.simulation import Simulation
from simulation.comparing_simulations import ComparingSimulations
from model_database_handler.model_database_handler import *
from data.stock_database import get_stocks


available_stocks = None


def nothing():
    pass


def render_title():
    print("""

     _                 _                        _ 
    | |               | |                      (_)
    | |_ _ __ __ _  __| | ___ _ __         __ _ _ 
    | __| '__/ _` |/ _` |/ _ \ '_ \       / _` | |
    | |_| | | (_| | (_| |  __/ | | |  _  | (_| | |
     \__|_|  \__,_|\__,_|\___|_| |_| (_)  \__,_|_|
  
  
        """)


def help_instructions():

    print("\n+\n|\t% Application Description\n|")
    print("|\t\tThis application presents a tool to simulate mathematical")
    print("|\t\ttrading models, using real data from previous years\n|")
    print("|\t% Commands\n|")
    print("|\t\th\tOpen the help instructions.\n|")
    print("|\t\ts\tCreate a stock trading model simulation.\n|")
    print("|\t\tx\tClear simulation history.\n|")
    print("|\t\tq\tQuit the application.\n+\n")


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
        if not all(item in available_stocks for item in stocks):
            print("\n\tPlease enter valid and available stocks.")
            continue
        return stocks


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def ask_period():
    while True:
        start_date = input("\nStart of the simulation: (YYYY-mm-dd) ")
        if not validate_date(start_date):
            print("\n\tPlease enter a valid date.")
            continue
        end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")
        if not validate_date(end_date):
            print("\n\tPlease enter a valid date.")
            continue
        return start_date, end_date


def ask_model_instances():
    while True:
        model_instances_raw = input("\nModel instance(s): ")
        model_instances_clean = re.split(", |,| ", model_instances_raw)
        if model_instances_raw.lower() == "l":
            print("\n\t% Available Models Instances\n")
            instances = list_instances()
            for i in instances:
                print("\t" + i)
            continue
        elif not all(item in list_instances() for item in model_instances_clean):
            print("\n\tPlease enter valid and available model instances.")
            print("\n\tInsert 'l' to consult them.")
            continue

        for i in range(len(model_instances_clean)):
            model_instances_clean[i] = get_instance(model_instances_clean[i])

        return model_instances_clean


def ask_executions():
    while True:
        try:
            no_exec = int(input("\nNumber of executions: "))
            return no_exec
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_graph():
    while True:
        option = input("Plot results into graph? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.")
            continue
        return option in ("yes", "y")


def ask_simulation():

    balance = ask_balance()
    stocks = ask_stocks()
    start_date, end_date = ask_period()
    model_instances = ask_model_instances()
    no_exec = ask_executions()

    try:
        if len(model_instances) == 1:
            do_simulation(balance, stocks, start_date, end_date, model_instances[0], no_exec)
        else:
            do_simulation_comparison(balance, stocks, start_date, end_date, model_instances, no_exec)

    except KeyboardInterrupt:
        print("\n\n\tAborted.\n")
    except Exception as e:
        print("\n\tAborted.\n\tCaught an exception while executing the simulation: " + str(e) + "\n")


def render_simulation_logs(sim: Simulation):

    logs_str = ""
    results = sim.get_results()
    logs_str += "\nEx."

    for execution, _ in enumerate(results, start=1):
        logs_str += "\n[{}]{}".format(execution, sim.logs_str(no_execution=execution - 1))

    return logs_str


def render_simulation_results(sim: Simulation):

    results_str = ""
    results = sim.get_results()
    results_str += "\nEx."

    for execution, result in enumerate(results, start=1):
        results_str += "\n[{}]\t\tProfit: {}".format(execution, result["profit"])
        results_str += "\n\t\tProfit (%): {}".format(result["profit_percentage"])
        results_str += "\n\t\tProfit (% / Year): {}\n".format(result["profit_percentage_year"])
        for stock in result["stocks_performance"]:
            results_str += "\n\t\tProfit for {} stock (%) : {}".format(stock, result["stocks_performance"][stock])

    return results_str


def store_simulation_results(sim: Simulation):
    try:
        if not os.path.exists("simulation_history/"):
            os.mkdir("simulation_history/")

        timestamp = datetime.now()
        filepath = "simulation_history/{}.txt".format(sim.get_model().__class__.__name__ + str(timestamp.year) +
                                                      str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) +
                                                      str(timestamp.minute) + str(timestamp.second) +
                                                      str(timestamp.microsecond))
        with open(filepath, 'w') as f:
            f.write("+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Details" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write("\nBalance: {}\nStocks: {}\nStarting Date: {}\nEnding Date: {}\nModel: {}\t({})\n".format(
                sim.get_initial_balance(), sim.get_tradable_stocks(), sim.get_start_date(), sim.get_end_date(),
                sim.get_model().__class__.__name__, sim.get_model().get_description()))
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Results" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_simulation_results(sim))
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 32) + "Simulation Logs" + (" " * 31) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_simulation_logs(sim))

        return filepath

    except Exception as e:
        return "ERROR: Could not store the simulation data: " + str(e)


def do_simulation(balance: float, stocks: list, start_date: str, end_date: str, model_instance, no_exec: int):

    try:
        sim = Simulation(balance, stocks, start_date, end_date, model_instance)
        sim.execute(no_executions=no_exec)

        print("\n\t\t% Simulation Results\n" + render_simulation_results(sim))
        print("For more details: " + store_simulation_results(sim) + "\n")

        if ask_graph():
            sim.get_graph()
        print("")

    except Exception as e:
        raise e


def render_comparison_results(comp: ComparingSimulations):

    results_str = ""
    best_sim = comp.get_best_simulation_by_metric()
    worst_sim = comp.get_worst_simulation_by_metric()

    results_str += "\n\t% Best model ({})\n".format(best_sim.get_model())
    results_str += render_simulation_results(best_sim)

    results_str += "\n\t% Worst model ({})\n".format(worst_sim.get_model())
    results_str += render_simulation_results(worst_sim)

    return results_str


def store_comp_results(comp: ComparingSimulations):

    filenames = ""
    sims = comp.get_simulations()
    filenames += store_simulation_results(sims[0])

    for sim in sims[1:]:
        filenames += ", "
        filenames += store_simulation_results(sim)

    return filenames


def do_simulation_comparison(balance: float, stocks: list, start_date: str, end_date: str, model_instances,
                             no_exec: int):
    try:
        sims = []
        for instance in model_instances:
            sims.append(Simulation(balance, stocks, start_date, end_date, instance))

        comp = ComparingSimulations(sims)
        comp.execute(no_executions=no_exec)

        print(render_comparison_results(comp))
        print("For more details: " + store_comp_results(comp) + "\n")

        if ask_graph():
            comp.get_graph_comparison()
        print("")

    except Exception as e:
        raise e


def clear_simulation_history():
    try:
        if os.path.isdir("simulation_history/"):
            files_raw = input("\nFiles to delete: (* for all) ")
            if files_raw == "*":
                for f in os.listdir("simulation_history/"):
                    os.remove(os.path.join("simulation_history/", f))
            else:
                files = re.split(", |,| ", files_raw.lower())
                for f in files:
                    filepath = "simulation_history/{}.txt".format(f)
                    if os.path.exists(filepath):
                        os.remove(filepath)
            print("\n\tSimulation history removed with success.\n")
        else:
            print("\n\tSimulation history not found.\n")

    except Exception as e:
        print("\n\tCaught an exception while deleting the simulation history: " + str(e) + "\n")


def quit_app():
    print("")
    exit()


def invalid_command():
    print("\n\tERROR: Invalid command.\n\tPlease insert 'h' for help.\n")


def parse_command(command: str):

    command_switcher = {
        "": nothing,
        "h": help_instructions,
        "s": ask_simulation,
        "x": clear_simulation_history,
        "q": quit_app
    }

    func = command_switcher.get(command, lambda: invalid_command())
    func()


def run():

    while True:
        try:
            command = input("traden.ai> ")
            parse_command(command)
        except KeyboardInterrupt:
            quit_app()


if __name__ == "__main__":
    available_stocks = set(get_stocks("../data/symbols.txt"))
    render_title()
    run()
