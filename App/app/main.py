import sys
from App.app.commands import Commands
from SimulationTester.main.simulation_frontend import SimulationFrontend

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


def parse_command(command: str):

    command_switcher = {
        "": commands.nothing,
        "h": commands.help_instructions,
        "s": commands.do_simulation,
        "xs": commands.close_simulation,
        "xi": commands.delete_model_instances,
        "p": commands.ctrl_ping,
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

    MAX_ARGS = 3
    args = sys.argv

    # Receive and print arguments
    print(f"Received {len(args)} arguments\n")
    for i in range(len(args)):
        print(f"arg[{i}] = {args[i]}")
        print("")

    # Check arguments
    if len(args) not in (MAX_ARGS - 1, MAX_ARGS):
        print("ERROR incorrect number of arguments.")
        print("Usage: python main.py simulation_host simulation_port\n")

    # Parse arguments
    simulation_host = args[1]
    simulation_port = args[2]

    frontend = SimulationFrontend(simulation_host, simulation_port)
    commands = Commands(frontend)
    render_title()
    run()
