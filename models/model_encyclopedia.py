from .ema import EMA
from .random_op import Random

model_docs = {
    "ema": {"class": EMA, "desc": "(...)"},
    "random": {"class": Random, "desc": "Buys and sells randomly."}
}


def models_str():
    if model_docs == {}:
        return "\tNo models available.\n"

    models_format = ""
    for key, value in model_docs.items():
        models_format += "\n\t\t{}: {}\n".format(key, value["desc"])

    return models_format
