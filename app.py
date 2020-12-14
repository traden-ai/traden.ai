import re
import models
import datetime as dt
from simulation import Simulation
from stock_database import data_download, data_update

def render_title():

    print("""\

 (                                                             (               
 )\ )   )            )    *   )          (                     )\ )            
 (()/(( /(         ( /(  ` )  /((      )  )\ ) (        (  (   (()/((     )     
 /(_))\())(    (  )\())  ( )(_))(  ( /( (()/( )\  (    )\))(   /(_))\   (      
 (_))(_))/ )\   )\((_)\  (_(_()|()\ )(_)) ((_)|(_) )\ )((_))\  (_))((_)  )\  '  
 / __| |_ ((_) ((_) |(_) |_   _|((_|(_)_  _| | (_)_(_/( (()(_) / __|(_)_((_))   
 \__ \  _/ _ \/ _|| / /    | | | '_/ _` / _` | | | ' \)) _` |  \__ \| | '  \()  
 |___/\__\___/\__||_\_\    |_| |_| \__,_\__,_| |_|_||_|\__, |  |___/|_|_|_|_(_) 
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
    print("|\t\tq\tQuit the application." + (" " * 34) + "|")
    print("|" + (" " * 78) + "|")
    print("+" + ("-" * 78) + "+\n")

def data_d():
    year = int(input("\nFrom what year do you pretend to download data? "))
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
    print("\n\t% Simulation Results %\n")

    for execution, result in enumerate(results, start=1):
        print("\tExecution {}".format(execution))
        print("\tProfit: {}".format(result["profit"]))
        print("\tProfit Percentage: {}".format(result["profit_percentage"]))
        print("\tLogs:\n{}".format(sim.logs_str(no_execution=execution-1)))

def simulation():
    
    balance = float(input("\n\tWhat is your initial balance? "))

    stocks_raw = input("\n\tWhat stocks do you intend to trade? ")
    stocks = re.split(", |,| ", stocks_raw.upper())
    
    start_date = input("\n\tWhen do you want to start the simulation? (YYYY-mm-dd) ")
    end_date = input("\n\tWhen do you want to end the simulation? (YYYY-mm-dd) ")

    buying_model = input("\n\tWhich buying model do you want to simulate? ")
    while buying_model not in models.model_docs:
        print("\n\tInvalid model. Please check the following list of available models...\n")
        print(models.models_str())
        buying_model = input("\tWhich buying model do you want to simulate? ")

    selling_model = input("\n\tWhich selling model do you want to simulate? ")
    while selling_model not in models.model_docs:
        print("\n\tInvalid model. Please check the following list of available models...\n")
        print(models.models_str())
        selling_model = input("\tWhich selling model do you want to simulate? ")

    # model = input("\nWhich model do you want to simulate? ")

    sim = Simulation(balance, stocks, start_date, end_date, models.model_docs[buying_model]["func"], models.model_docs[selling_model]["func"])

    no_exec = int(input("\n\tHow many executions do you want to simulate? "))

    sim.execute(no_exec)

    render_simulation_results(sim)

def quit_app():
    print("")
    exit()

def invalid_command():
    print("\nInvalid command. Please insert 'h' for help.\n")

def parse_command(command: str):
    
    command_switcher = {
        "": nothing,
        "h": help_instructions,
        "d": data_d,
        "u": data_u,
        "s": simulation,
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
