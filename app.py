import os
import re
import datetime as dt
from simulation import Simulation
from models import model_encyclopedia
from comparing_simulations import ComparingSimulations
from stock_database import data_download, data_update

sim_id = 1

def get_last_sim_id():
    global sim_id
    while os.path.exists(f"results/s{sim_id}.txt"):
        sim_id += 1

def update_sim_id():
    global sim_id
    sim_id += 1

def render_title():

    print("""\

  _____ _             _     _____             _ _               _____ _               
 /  ___| |           | |   |_   _|           | (_)             /  ___(_)              
 \ `--.| |_ ___   ___| | __  | |_ __ __ _  __| |_ _ __   __ _  \ `--. _ _ __ ___      
  `--. \ __/ _ \ / __| |/ /  | | '__/ _` |/ _` | | '_ \ / _` |  `--. \ | '_ ` _ \     
 /\__/ / || (_) | (__|   <   | | | | (_| | (_| | | | | | (_| | /\__/ / | | | | | | _ 
 \____/ \__\___/ \___|_|\_\  \_/_|  \__,_|\__,_|_|_| |_|\__, | \____/|_|_| |_| |_|(_)
                                                         __/ |                        
                                                        |___/                         
        """)

def nothing():
    pass

def help_instructions():
    print("\n+" + ("-" * 78) + "+")
    print("|" + (" " * 37) + "Help" + (" " * 37) + "|")
    print("+" + ("-" * 78) + "+")
    print("|" + (" " * 78) + "|")
    print("|\tDescription:" + (" " * 59) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\tThis application presents a tool to simulate mathematical" + (" " * 6) + "|")
    print("|\t\ttrading models, using real data from previous years." + (" " * 11) + "|")
    print("|" + (" " * 78) + "|")
    print("|\tThe options are as follows:" + (" " * 44) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\th\tOpen the help instructions." + (" " * 28) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\td\tDownload data since a year of your choice." + (" " * 13) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\tu\tUpdate the data for the current year." + (" " * 18) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\ts\tCreate a stock trading simulation." + (" " * 21) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\tc\tCompare multiple simulations." + (" " * 26) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\tx\tClear simulation history." + (" " * 30) + "|")
    print("|" + (" " * 78) + "|")
    print("|\t\tq\tQuit the application." + (" " * 34) + "|")
    print("|" + (" " * 78) + "|")
    print("+" + ("-" * 78) + "+\n")

def data_d():
    year = int(input("\nStarting year for data download: "))
    if year <= int(dt.date.today().strftime("%Y")) and year > 0:
        data_download(year)
        print("")
    else:
        print("\nInvalid year.\n")

def data_u():
    data_update()
    print("")

def ask_balance():
    try:
        balance = float(input("\nInitial balance: "))
        return balance
    except Exception as e:
        raise e

def ask_stocks():
    try:
        stocks_raw = input("\nStocks: ")
        stocks = re.split(", |,| ", stocks_raw.upper())
        return stocks
    except Exception as e:
        raise e

def ask_period():
    try:
        start_date = input("\nStart of the simulation: (YYYY-mm-dd) ")
        end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")
        return start_date, end_date
    except Exception as e:
        raise e

def ask_model():
    try:
        model = input("\nSimulation Model: ")
        model = model.lower()
        while model not in model_encyclopedia.model_docs:
            if model == "l":
                print("\n\t% Available Models %")
                print(model_encyclopedia.models_str())
            else:
                print("\n\tERROR: Invalid model.\n\tPlease insert 'l' for a list of the available models.\n")
            model = input("Simulation Model: ")
        return model
    except Exception as e:
        raise e

def ask_multiple_models():
    try:
        models_raw = input("\nModels to compare: ")
        models_clean = re.split(", |,| ", models_raw.lower())
        while len(models_clean) < 2 or not all(item in model_encyclopedia.model_docs.keys() for item in models_clean):
            if models_raw.lower() == "l":
                print("\n\t% Available Models %")
                print(model_encyclopedia.models_str())
            elif len(models_clean) < 2 and all(item in model_encyclopedia.model_docs.keys() for item in models_clean):
                print("\n\tERROR: Invalid input.\n\tPlease insert enough models for a comparison.\n")
            else:
                print("\n\tERROR: Invalid model.\n\tPlease insert 'l' for a list of the available models.\n")
            models_raw = input("Models to compare: ")
            models_clean = re.split(", |,| ", models_raw)
        return models_clean
    except Exception as e:
        raise e

def ask_executions():
    try:
        no_exec = int(input("\nNumber of executions: "))
        return no_exec
    except Exception as e:
        raise e

def ask_graph(graph_type="results"):
    try:
        graph = input("Plot {} into graph? (yes/no) ".format(graph_type))
        while graph not in ("yes", "no", "y", "n"):
            graph = input("Plot {} into graph? (yes/no) ".format(graph_type))
        return graph
    except Exception as e:
        raise e

def render_simulation_logs(sim: Simulation):
    logs_str = ""
    results = sim.get_results()
    logs_str += "\nEx."

    for execution, _ in enumerate(results, start=1):
        logs_str += "\n[{}]{}".format(execution, sim.logs_str(no_execution=execution-1))

    return logs_str

def render_simulation_long_results(sim: Simulation):
    results_str = ""
    results = sim.get_results()
    results_str += "\nEx."

    for execution, result in enumerate(results, start=1):
        results_str += "\n[{}]\tProfit: {}".format(execution, result["profit"])
        results_str += "\n\tProfit (%): {}".format(result["profit_percentage"])
        results_str += "\n\tProfit (% / Year): {}\n".format(result["profit_percentage_year"])

    return results_str

def store_sim_results(sim: Simulation):

    try:
        if not os.path.exists("results/"):
            os.mkdir("results/")

        filepath = "results/s{}.txt".format(sim.get_id())
        with open(filepath,'w') as f:
            f.write("+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Details" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write("\nBalance: {}\nStocks: {}\nStarting Date: {}\nEnding Date: {}\nModel: {}\t({})\n".format(\
                sim.get_initial_balance(), sim.get_tradable_stocks(), sim.get_start_date(), sim.get_end_date(), sim.get_model(), model_encyclopedia.model_docs[sim.get_model().lower()]["desc"]))
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 30) + "Simulation Results" + (" " * 30) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_simulation_long_results(sim))
            f.write("\n+" + ("-" * 78) + "+\n")
            f.write("|" + (" " * 32) + "Simulation Logs" + (" " * 31) + "|\n")
            f.write("+" + ("-" * 78) + "+\n")
            f.write(render_simulation_logs(sim))

        return filepath
    
    except:
        return "Error occurred when storing the simulation data..."
        
def simulation():
    try:
        balance = ask_balance()
        stocks = ask_stocks()
        start_date, end_date = ask_period()
        model = ask_model()
        no_exec = ask_executions()

        update_sim_id()
        sim = Simulation(sim_id, balance, stocks, start_date, end_date, model_encyclopedia.model_docs[model]["class"])
        sim.execute(no_executions=no_exec)

        print("\n\t% Simulation Results %\n" + render_simulation_long_results(sim))
        print("For more details: " + store_sim_results(sim) + "\n")

        graph = ask_graph(graph_type="simulation")
        if graph in ("yes", "y"):
            sim.get_graph()
        print("")

    except:
        if KeyboardInterrupt:
            print("")
        print("\n\tAborted.\n\tSomething went wrong with your simulation...\n")

def render_comparison_menu():
    menu_str = ""
    menu_str += "\n\t% Types of comparisons available %\n"
    menu_str += "\n\t[1] Compare simulation models (for same stocks and time period)\n"
    menu_str += "\n\t[2] Compare time periods (for same stocks and model)\n"
    menu_str += "\n\t[3] Compare stocks (for same model and time period)\n"
    return menu_str

def render_comparison_short_results(comp: ComparingSimulations, comp_type="id"):
    def get_title(sim: Simulation, comp_type="id"):
        title = ""
        if comp_type == "id":
            title += str(sim.get_id())
        elif comp_type == "model":
            title += sim.get_model()
        elif comp_type == "period":
            title += sim.get_start_date() + " -> " + sim.get_end_date()
        elif comp_type == "stock":
            title += sim.get_stocks()[0]
        return title

    results_str = ""
    best_sim = comp.get_best_simulation_by_metric()
    worst_sim = comp.get_worst_simulation_by_metric()

    results_str += "\n\t% Best {} ({}) %\n".format(comp_type, get_title(best_sim, comp_type=comp_type))
    results_str += render_simulation_long_results(best_sim)

    results_str += "\n\t% Worst {} ({}) %\n".format(comp_type, get_title(worst_sim, comp_type=comp_type))
    results_str += render_simulation_long_results(worst_sim)

    return results_str

def render_comparison_long_results(comp: ComparingSimulations, comp_type="id"):
    #TODO
    return ""

def store_comp_results(comp: ComparingSimulations):
    
    filenames = ""
    sims = comp.get_simulations()
    filenames += store_sim_results(sims[0])

    for sim in sims[1:]:
        filenames += ", "
        filenames += store_sim_results(sim)

    return filenames

def compare_type_one():
    try:
        balance = ask_balance()
        stocks = ask_stocks()
        start_date, end_date = ask_period()
        models_clean = ask_multiple_models()
        no_exec = ask_executions()

        sims = []
        for model in models_clean:
            update_sim_id()
            sims.append(Simulation(sim_id, balance, stocks, start_date, end_date, model_encyclopedia.model_docs[model]["class"]))

        comp = ComparingSimulations(sims)
        comp.execute(no_executions=no_exec)

        print(render_comparison_short_results(comp, comp_type="model"))
        print("For more details: " + store_comp_results(comp) + "\n")

        graph = ask_graph(graph_type="comparison")
        if graph in ("yes", "y"):
            comp.get_graph_comparison(label="model")
        print("")

    except Exception as e:
        raise e

def compare_type_two():
    #TODO
    pass

def compare_type_three():
    #TODO
    pass

def compare_sims():
    
    print(render_comparison_menu())

    try:
        comp_type = int(input("Select type: "))

        if comp_type == 1:
            compare_type_one()
        elif comp_type == 2:
            compare_type_two()
        elif comp_type == 3:
            compare_type_three()
        else:
            print("\n\tERROR: Type of comparison does not exist.")
            compare_sims()
            return
    except:
        if KeyboardInterrupt:
            print("")
        print("\n\tAborted.\n\tSomething went wrong with your comparison...\n")

def results_clear():

    files_raw = input("\nFiles to delete: (* for all OR s1, s2, ...) ")
    if files_raw == "*":
        for f in os.listdir("results/"):
            os.remove(os.path.join("results/", f))
    else:
        files = re.split(", |,| ", files_raw.lower())
        for f in files:
            filepath = "results/{}.txt".format(f)
            if os.path.exists(filepath):
                os.remove(filepath)
    print("")

def quit_app():
    print("")
    exit()

def invalid_command():
    print("\n\tERROR: Invalid command.\n\tPlease insert 'h' for help.\n")

def parse_command(command: str):
    
    command_switcher = {
        "": nothing,
        "h": help_instructions,
        "d": data_d,
        "u": data_u,
        "s": simulation,
        "c": compare_sims,
        "x": results_clear,
        "q": quit_app
    }

    func = command_switcher.get(command, lambda: invalid_command())
    func()

def run():
    while True:
        try:
            command = input("stock_trading> ")
        except:
            print("")
            continue
        parse_command(command)

if __name__ == "__main__":
    get_last_sim_id()
    render_title()
    run()
