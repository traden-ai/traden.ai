import os
import jsonpickle
from models.model_interface import ModelInterface

path = "instances/"


def get_instance(name: str):
    with open(path + name, 'r') as f:
        json_string = f.read()
    return jsonpickle.decode(json_string)


def save_instance(name: str, instance: ModelInterface):
    json_string = jsonpickle.encode(instance)
    with open(path + name, 'w') as f:
        f.write(json_string)


def delete_instance(name: str):
    filepath = path + name
    if os.path.exists(filepath):
        os.remove(filepath)


def list_instances():
    return os.listdir(path)
