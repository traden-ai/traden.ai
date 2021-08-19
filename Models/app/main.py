import sys


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


def ask_mode():
    while True:
        mode = input("traden.ai> ")
        if (mode == "ci"):
            pass
        elif (mode == "cu"):
            pass
        elif (mode == "ca"):
            pass
        elif (mode == "t"):
            pass
        elif (mode == "n"):
            pass
        elif (mode == "q"):
            quit_app()
        else:
            print("\n+\n|\t% Application Description\n|")
            print("|\t\tThis application presents a tool to simulate mathematical")
            print("|\t\ttrading models, using real data from previous years\n|")
            print("|\t% Commands\n|")
            print("|\t\tci\tConvert instance into univariate model.\n|")
            print("|\t\tcu\tCreate composition of univariate models.\n|")
            print("|\t\tca\tCreate allocator and save allocator.\n|")
            print("|\t\tt\tTrainable models specifics.\n|")
            print("|\t\tn\tNot trainable models specifics.\n|")
            print("|\t\tq\tQuit application.\n+\n")

def run():
    commands = None

    while True:
        try:
            if commands is None:
                commands = ask_mode()

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
    render_title()
    run()