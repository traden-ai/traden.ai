import sys

from Models.app.model_helper.commands import convert_instance_into_univariate_model, \
    create_composition_of_univariate_models, create_allocator_and_save_allocator, save_instance, \
    train_and_save_instance, test_instance, test_estimator, stack_multiple_estimators, save_sel_instance, \
    train_existing_instance


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


def execute():
    while True:
        mode = input("traden.ai> ")
        if (mode == "ci"):
            convert_instance_into_univariate_model()
        elif (mode == "cu"):
            create_composition_of_univariate_models()
        elif (mode == "ca"):
            create_allocator_and_save_allocator()
        elif (mode == "t"):
            execute_trainable_specifics()
        elif (mode == "n"):
            execute_non_trainable_specifics()
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

def execute_trainable_specifics():
    while True:
        mode = input("traden.ai> trainable specifics> ")
        if (mode == "ts"):
            train_and_save_instance()
        elif (mode == "ti"):
            test_instance()
        elif (mode == "tei"):
            train_existing_instance()
        elif (mode == "te"):
            test_estimator()
        elif (mode == "se"):
            stack_multiple_estimators()
        elif (mode == "q"):
            execute()
        else:
            print("\n+\n|\t% Application Description\n|")
            print("|\t\tThis application presents a tool to simulate mathematical")
            print("|\t\ttrading models, using real data from previous years\n|")
            print("|\t% Commands\n|")
            print("|\t\tts\tTrain and Save Instance.\n|")
            print("|\t\ttei\tTrain Existing Instance.\n|")
            print("|\t\tti\tTest Instance.\n|")
            print("|\t\tte\tTest Estimator.\n|")
            print("|\t\tse\tStack Multiple Estimators.\n|")
            print("|\t\tq\tQuit application.\n+\n")


def execute_non_trainable_specifics():
    while True:
        mode = input("traden.ai> non trainable specifics> ")
        if (mode == "s"):
            save_sel_instance()
        elif (mode == "q"):
            execute()
        else:
            print("\n+\n|\t% Application Description\n|")
            print("|\t\tThis application presents a tool to simulate mathematical")
            print("|\t\ttrading models, using real data from previous years\n|")
            print("|\t% Commands\n|")
            print("|\t\ts\tSave Instance.\n|")
            print("|\t\tq\tQuit application.\n+\n")


def run():

    while True:
        try:
            execute()
        except KeyboardInterrupt:
            quit_app()


if __name__ == "__main__":
    render_title()
    run()