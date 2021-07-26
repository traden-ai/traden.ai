import sys
from App.simulation.commands import SimulationCommands
from App.exchange.commands import ExchangeCommands
from SimulationTester.main.simulation_frontend import SimulationFrontend
from ExchangeTester.main.exchange_frontend import ExchangeFrontend



def render_title():
    print("""

     _                 _                        _ 
    | |               | |                      (_)
    | |_ _ __ __ _  __| | ___ _ __         __ _ _ 
    | __| '__/ _` |/ _` |/ _ \ '_ \       / _` | |
    | |_| | | (_| | (_| |  __/ | | |  _  | (_| | |
     \__|_|  \__,_|\__,_|\___|_| |_| (_)  \__,_|_|
  
  
        """)


def quit_app():
    print("")
    exit()


def invalid_command():
    print("\n\tERROR: Invalid command.\n\tPlease insert 'h' for help.\n")


def ask_mode(sim, exc):
    while True:
        mode = input("traden.ai> ")
        if (mode == "e"):
            return exc
        elif (mode == "s"):
            return sim
        elif (mode == "q"):
            quit_app()
        else:
            print("\n+\n|\t% Application Description\n|")
            print("|\t\tThis application presents a tool to simulate mathematical")
            print("|\t\ttrading models, using real data from previous years\n|")
            print("|\t% Commands\n|")
            print("|\t\ts\tEnter simulation mode.\n|")
            print("|\t\te\tEnter exchange mode.\n|")
            print("|\t\tq\tQuit application.\n+\n")


def run(sim, exc):

    sim_commands = SimulationCommands(sim)
    exc_commands = ExchangeCommands(exc)
    commands = None

    while True:
        try:
            if commands is None:
                commands = ask_mode(sim_commands, exc_commands)

            command = input(commands.prompt())
            func = commands.parser(command)
            # FIXME use OK/NOK
            if func is None:
                commands = None
            else:
                func()

        except KeyboardInterrupt:
            quit_app()


if __name__ == "__main__":

    MAX_ARGS = 5
    args = sys.argv

    # Receive and print arguments
    print(f"Received {len(args)} arguments\n")
    for i in range(len(args)):
        print(f"arg[{i}] = {args[i]}")
        print("")

    # Check arguments
    if len(args) < MAX_ARGS or len(args) > MAX_ARGS:
        print("ERROR incorrect number of arguments.")
        print("Usage: python main.py simulation_host simulation_port exchange_host exchange_port\n")

    # Parse arguments
    simulation_host = args[1]
    simulation_port = args[2]
    exchange_host = args[3]
    exchange_port = args[4]

    sim_frontend = SimulationFrontend(simulation_host, simulation_port)
    exc_frontend = None
    #exc_frontend = ExchangeFrontend(exchange_host, exchange_port)
    
    render_title()
    run(sim_frontend, exc_frontend)
