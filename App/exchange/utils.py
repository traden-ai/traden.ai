from App.utils import *

def ask_model(instances):

    while True:
        instances = ask_model_instances(instances)
        
        if (len(instances) > 1):
            print("Please choose a single model")
            continue
        
        return instances

# TODO specify utils
