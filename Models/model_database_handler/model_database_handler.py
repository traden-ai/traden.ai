import os
import jsonpickle

from constants import PYTHON_PATH
from Models.models.interfaces.model_interface import ModelInterface
from Models.models import *
import inspect
import json

path = PYTHON_PATH + "/Models/instances/"


def get_instance(name: str):
    if os.path.exists(path + name):
        with open(path + name, 'r') as f:
            json_string = f.read()
        instance = jsonpickle.decode(json_string)
        instance.retrieve_attributes()
        return instance
    else:
        return None


def save_instance(name: str, instance: ModelInterface):
    instance.save_attributes()
    json_string = jsonpickle.encode(instance)
    json_content = json.loads(json_string)
    json_content["py/object"] = str(inspect.getfile(instance.__class__)).replace(PYTHON_PATH, "")\
        .replace("/", ".")[:-2] + str(instance.__class__.__name__)
    if json_content["py/object"][0] == ".":
        json_content["py/object"] = json_content["py/object"][1:]
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + name, 'w') as f:
        f.write(json.dumps(json_content))


def delete_instance(name: str):
    if os.path.exists(path + name):
        os.remove(os.path.join(path, name))


def delete_all():
    if os.path.exists(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))


def list_instances():
    if not os.path.exists(path):
        os.mkdir(path)
    elements = os.listdir(path)
    instances = []
    for element in elements:
        if "." not in element:
            instances.append(element)
    return instances
