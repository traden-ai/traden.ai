from datetime import datetime
from typing import re

import numpy as np

from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Models.model_database_handler.model_database_handler import list_instances, get_instance, save_instance
import importlib, inspect
import matplotlib.pyplot as plt
import os
import tensorflow as tf

def do_monte_carlo_simuls(Y_pred, Y_corr, N=1000):
    results = []
    my_result = minimum_squared_error(Y_pred, Y_corr)
    for i in range(N):
        np.random.shuffle(Y_pred)
        results.append(float(minimum_squared_error(Y_pred, Y_corr)))
    results.sort()
    for i in range(len(results)):
        if results[i] >= my_result:
            return (i / N) * 100
    return 100

def ask_test_parameters(instances: list):
    stock, start_date, end_date, pred_time = ask_preprocessing_parameters()
    model_instance = ask_model_instance(instances)
    ins = get_instance(model_instance)

    return stock, start_date, end_date, pred_time, ins

def ask_stock():
    stock_raw = input("\n\tStock: ")
    stock = stock_raw.upper()
    return stock

def ask_model_instance(instances):

    while True:
        model_instance_raw = input("\n\tModel instance: ")
        if model_instance_raw.lower() == "l":
            print("\n\t% Available Models Instances\n")
            if instances:
                for i, ins in enumerate(instances, start=1):
                    print("\t[" + str(i) + "]\t" + ins)
            else:
                print("\tSorry. No model instances available.")
            continue
        elif (not model_instance_raw in instances) and not (model_instance_raw.isdigit() and int(model_instance_raw) in range(1, len(instances) + 1)):
            print("\n\tERROR: Invalid model instance(s).")
            print("\tPlease insert 'l' to consult the available instances.")
            continue

        return model_instance_raw if not model_instance_raw.isdigit() else instances[int(model_instance_raw) - 1]

def ask_period():
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    while True:
        start_date = input("\n\tStart of the simulation: (YYYY-mm-dd) ")
        if not validate_date(start_date):
            print("\n\tPlease enter a valid date.")
            continue
        break
    while True:
        end_date = input("\n\tEnd of the simulation: (YYYY-mm-dd) ")
        if not validate_date(end_date):
            print("\n\tPlease enter a valid date.")
            continue
        return start_date, end_date

def ask_data_type():
    data_types = ("standard", "variation", "percentile")
    while True:
        data_type = input("\n\tData Type: ")
        if data_type.lower() == "l":
            print("\n\t% Available Data Types\n")
            for i, data_type in enumerate(data_types, start=1):
                print("\t[" + str(i) + "]\t" + data_type)
            continue
        elif not data_type in data_types or data_type.isdigit() and int(
            data_type) in range(1, len(data_types) + 1):
            print("\n\tERROR: Invalid data type.")
            print("\tPlease insert 'l' to consult the available data types.")
            continue
    return [data_type if not data_type.isdigit() else data_types[int(data_type) - 1]]

def ask_instance_parameters():
    while True:
        no = input("\n\tNumber of parameters: ")
        parameters = []
        if no.isdigit():
            for i in range(int(no)):
                parameters.append(input("\n\tParameter {}: ".format(i)))
            break
    return parameters

def ask_preprocessing_parameters():
    stock = ask_stock()
    start_date, end_date = ask_period()
    pred_time = ask_pred_time()
    return [stock, start_date, end_date, pred_time]


def ask_pred_time():
    pred_time = input("\n\tPredTime: ")
    return pred_time

def ask_no_models():
    while True:
        no = input("\tNumber of models?")
        if not no.isdigit():
            continue
        return no

def ask_graph():
    while True:
        option = input("\tPlot results into graph? (yes/no) ")
        if option not in ("yes", "no", "y", "n"):
            print("\n\tPlease enter valid option.\n")
            continue
        return option in ("yes", "y")

def render_graph(correct_data, predicted_data):
    plt.xlabel("DataPoints")
    plt.ylabel("TargetPoints")
    plt.plot(range(len(correct_data)), correct_data, label=f"CorrectData")
    plt.plot(range(len(predicted_data)), predicted_data, label=f"PredictedData")
    plt.legend(loc='best')
    plt.show()

def list_model_classes(file):
    classes = []
    for name, cls in inspect.getmembers(importlib.import_module(file), inspect.isclass):
        if cls.__module__ == file:
            classes.append((name, cls))
    return classes

def list_model_classes_from_folder(relative_path, raw_absolute_path):
    clean_absolute_path = raw_absolute_path.replace("/", ".")
    files = filter(lambda el: el.find(".py") != -1 , os.listdir(relative_path))
    classes = []
    for file in files:
        classes += list_model_classes(clean_absolute_path + file.replace(".py", ""))
    return classes

def minimum_squared_error(y_pred, y_corr):
    squared_difference = tf.square(y_corr - y_pred)
    return tf.reduce_mean(squared_difference, axis=-1)