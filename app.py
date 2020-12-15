import os
import re
import models
import datetime as dt
from simulation import Simulation
from stock_database import data_download, data_update

sim_ID = 1

def update_sim_ID():
    global sim_ID
    while os.path.exists(f"results/s_{sim_ID}.txt"):
        sim_ID += 1

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

def store_results(sim: Simulation, sim_ID: int, balance: int, stocks: list, start_date: str, end_date: str, model: str):

    if not os.path.exists("results/"):
        os.mkdir("results/")

    filepath = "results/s_{}.txt".format(sim_ID)
    with open(filepath,'w') as f:
        f.write("+" + ("-" * 78) + "+\n")
        f.write("|" + (" " * 30) + "Simulation Details" + (" " * 30) + "|\n")
        f.write("+" + ("-" * 78) + "+\n")
        f.write("\nBalance: {}\nStocks: {}\nStarting Date: {}\nEnding Date: {}\nModel: {}\t({})\n".format(\
            balance, stocks, start_date, end_date, model, models.model_docs[model]["desc"]))
        f.write("\n+" + ("-" * 78) + "+\n")
        f.write("|" + (" " * 30) + "Simulation Results" + (" " * 30) + "|\n")
        f.write("+" + ("-" * 78) + "+\n")
        f.write(render_simulation_long_results(sim))
        f.write("\n+" + ("-" * 78) + "+\n")
        f.write("|" + (" " * 32) + "Simulation Logs" + (" " * 31) + "|\n")
        f.write("+" + ("-" * 78) + "+\n")
        f.write(render_simulation_logs(sim))

    return filepath
        
def simulation():
    
    balance = float(input("\nInitial balance: "))

    stocks_raw = input("\nStocks: ")
    stocks = re.split(", |,| ", stocks_raw.upper())
    
    start_date = input("\nStart of the simulation: (YYYY-mm-dd) ")
    end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")

    model = input("\nSimulation Model: ")
    while model not in models.model_docs:
        if model == "l":
            print("\n% Available Models %")
            print(models.models_str())
        else:
            print("\nERROR: Invalid model.\nPlease insert 'l' for a list of the available models.\n")
        model = input("Simulation Model: ")

    update_sim_ID()
    sim = Simulation(sim_ID, balance, stocks, start_date, end_date, models.model_docs[model]["func"])
    no_exec = int(input("\nNumber of executions: "))

    sim.execute(no_exec)
    print("\n" + "% Simulation Results %\n" + render_simulation_long_results(sim))
    print("For more details: " + store_results(sim, sim_ID, balance, stocks, start_date, end_date, model) + "\n")

def compare_sims():
    #TODO
    pass

def results_clear():

    files_raw = input("\nFiles to delete: (* for all OR s_1, c_1_2, ...) ")
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
        command = input("stock_trading> ")
        parse_command(command)

if __name__ == "__main__":
    render_title()
    run()
