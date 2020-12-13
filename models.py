
def buyAll(simulation):
    simulation.buy("AMZN", 1)
    """
    from random import randint
    if randint(0,1):
        simulation.buy("AMZN", 1)
    else:
        simulation.sell("AMZN", 1)"""

def void(simulation):
    return None

model_docs = {
        "buyAll": {"func": buyAll, "desc": "Buys everytime."},
        "void": {"func": void, "desc": "Does nothing."}
    }

def models_str():
    
    if model_docs == {}:
        return "\tNo models available."

    models_format = ""
    for key, value in model_docs.items():
        models_format += "\t{}\t\t{}\n".format(key, value["desc"])
    
    return models_format
