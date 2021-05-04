import os
import jsonpickle
from models.model_interface import ModelInterface
from models import *

path = "../instances/"


def get_instance(name: str):
    with open(path + name, 'r') as f:
        json_string = f.read()
    instance = jsonpickle.decode(json_string)
    instance.retrieve_attributes()
    return instance


def save_instance(name: str, instance: ModelInterface):
    instance.save_attributes()
    json_string = jsonpickle.encode(instance)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + name, 'w') as f:
        f.write(json_string)


def delete_instance(name: str):
    if os.path.exists(path + name):
        os.remove(os.path.join(path, name))


def delete_all():
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))


def list_instances():
    return os.listdir(path)
