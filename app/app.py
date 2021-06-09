import re
from datetime import datetime
from simulation.simulation import Simulation
from simulation.simulation_assembler import SimulationAssembler
from model_database_handler.model_database_handler import *
from utils.utils import get_stocks

available_stocks = None
symbols_path = PYTHON_PATH + "/data/symbols.txt"


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
    print("|\t\txh\tClear simulation history.\n|")
    print("|\t\txi\tClear model instances.\n|")
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
        break
    while True:
        end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")
        if not validate_date(end_date):
            print("\n\tPlease enter a valid date.")
            continue
        return start_date, end_date


def ask_model_instances():
    instances = list_instances()
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

        for i in range(len(model_instances_clean)):
            instance = model_instances_clean[i]
            if instance.isdigit():
                instance = instances[int(instance) - 1]
            model_instances_clean[i] = get_instance(instance)

        return model_instances_clean


def ask_executions():
    while True:
        try:
            no_exec = int(input("\nNumber of executions: "))
            return no_exec
        except ValueError:
            print("\n\tPlease enter a number.")


def ask_simulation():
    balance = ask_balance()
    stocks = ask_stocks()
    start_date, end_date = ask_period()
    model_instances = ask_model_instances()
    no_exec = ask_executions()

    return balance, stocks, start_date, end_date, model_instances, no_exec


def ask_results():
    while True:
        option = input("Store simulation results? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")


def ask_graph():
    while True:
        option = input("Plot results into graph? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")


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
    avg_results = sim.get_avg_results()
    results_str += "\nAvg:" if sim.get_no_executions() != 1 else "\nEx:\t"

    results_str += "\tProfit: {}".format(avg_results["profit"])
    results_str += "\n\t\tProfit (%): {}".format(avg_results["profit_percentage"])
    results_str += "\n\t\tProfit (% / Year): {}".format(avg_results["profit_percentage_year"])
    results_str += "\n\t\tOperating time (%): {}\n".format(avg_results["operating_time_percentage"])

    for stock in results[0]["stocks_performance"]:
        results_str += "\n\t\tProfit for {} stock (%): {}".format(stock, results[0]["stocks_performance"][stock])

    results_str += "\n"
    if len(sim.get_tradable_stocks()) > 1:
        results_str += "\t\tAverage profit for chosen stocks (%): {}\n".format(
            avg_results["stocks_performance"])

    return results_str


def store_simulation_results(sim: Simulation):
    try:
        dir_path = PYTHON_PATH + "/app/simulation_history/"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        filepath = dir_path + sim.get_model().__class__.__name__ + get_storing_index(sim.get_model().__class__.__name__)

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


def get_storing_index(name: str):
    res = 0

    dir_path = PYTHON_PATH + "/app/simulation_history/"
    if not os.path.exists(dir_path):
        return str(res)

    elements = os.listdir(dir_path)
    elements = [file for file in elements if file.startswith(name)]

    for el in elements:
        res = max(res, int(el.replace(name, "")) + 1)

    return str(res)


def render_comparison_results(comp: SimulationAssembler):
    results_str = ""
    sims = comp.get_ordered_simulations()

    for sim in sims:
        results_str += "\n\t\t% {}\n".format(sim.get_model().__class__.__name__)
        results_str += render_simulation_results(sim)

    return results_str


def store_comp_results(comp: SimulationAssembler):
    filenames = "\n\t"
    sims = comp.get_simulations()
    filenames += store_simulation_results(sims[0])

    for sim in sims[1:]:
        filenames += ",\n\t"
        filenames += store_simulation_results(sim)

    return filenames


def do_simulation():

    balance, stocks, start_date, end_date, model_instances, no_exec = ask_simulation()

    try:
        assembler = SimulationAssembler(balance, stocks, start_date, end_date, model_instances)
        assembler.execute(no_executions=no_exec)

        print(render_comparison_results(assembler))

        if ask_results():
            print("\n\tResults stored at: " + store_comp_results(assembler) + "\n")
        else:
            print("")

        if ask_graph():
            assembler.get_graph_comparison()
        print("")

    except KeyboardInterrupt:
        print("\n\n\tAborted.\n")
    except Exception as e:
        print("\n\tAborted.\n\tCaught an exception while executing the simulation: " + str(e) + "\n")
        raise e


def clear_simulation_history():
    delete_files(PYTHON_PATH + "/app/simulation_history/")


def clear_model_instances():
    delete_files(PYTHON_PATH + "/instances/")


def delete_files(dir_path: str):
    try:
        if os.path.isdir(dir_path):
            files_raw = input("\nFiles to remove: (* for all) ")
            if files_raw == "":
                print()
                return
            elif files_raw == "*":
                for f in os.listdir(dir_path):
                    os.remove(os.path.join(dir_path, f))
            else:
                files = re.split(", |,| ", files_raw)
                for f in files:
                    filepath = dir_path + f
                    if os.path.exists(filepath):
                        os.remove(filepath)
            print("\n\tFiles removed with success.\n")
        else:
            print("\n\tNo files found.\n")

    except Exception as e:
        print("\n\tCaught an exception while deleting designated files: " + str(e) + "\n")
        # raise e


def quit_app():
    print("")
    exit()


def invalid_command():
    print("\n\tERROR: Invalid command.\n\tPlease insert 'h' for help.\n")


def parse_command(command: str):
    command_switcher = {
        "": nothing,
        "h": help_instructions,
        "s": do_simulation,
        "xh": clear_simulation_history,
        "xi": clear_model_instances,
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
    available_stocks = set(get_stocks(symbols_path))
    render_title()
    run()
