import re
import models
import datetime as dt
from simulation import Simulation
from stock_database import data_download, data_update

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

def render_simulation_results(sim: Simulation):
    results = sim.get_results()
    print("\nEx.\t% Results %\n")

    for execution, result in enumerate(results, start=1):
        print("[{}]\tProfit: {}".format(execution, result["profit"]))
        print("\tProfit (%): {}".format(result["profit_percentage"]))
        print("\tProfit (% / Year): {}\n".format(result["profit_percentage_year"]))

def store_results(sim: Simulation):
    #TODO
    pass

def simulation():
    
    balance = float(input("\nInitial balance: "))

    stocks_raw = input("\nStocks: ")
    stocks = re.split(", |,| ", stocks_raw.upper())
    
    start_date = input("\nStart of the simulation: (YYYY-mm-dd) ")
    end_date = input("\nEnd of the simulation: (YYYY-mm-dd) ")

    buying_model = input("\nBuying model: ")
    while buying_model not in models.model_docs:
        if buying_model == "l":
            print("\n\t% Available Models %")
            print(models.models_str())
        else:
            print("\n\tERROR: Invalid model.\n\tPlease insert 'l' for a list of the available models.\n")
        buying_model = input("Buying model: ")

    selling_model = input("\nSelling model: ")
    while selling_model not in models.model_docs:
        if selling_model == "l":
            print("\n% Available Models %")
            print(models.models_str())
        else:
            print("\nERROR: Invalid model.\nPlease insert 'l' for a list of the available models.\n")
        selling_model = input("Selling model: ")

    sim = Simulation(balance, stocks, start_date, end_date, models.model_docs[buying_model]["func"], models.model_docs[selling_model]["func"])
    no_exec = int(input("\nNumber of executions: "))

    sim.execute(no_exec)
    render_simulation_results(sim)
    store_results(sim)

def compare_sims():
    #TODO
    pass

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
