import numpy as np

from Models.app.model_helper.utils import list_model_classes_from_folder, ask_model_instance, ask_test_parameters, \
    ask_instance_parameters, ask_preprocessing_parameters, ask_graph, render_graph
from Models.model_data_endpoint.model_data_endpoint import ModelDataEndpoint
from Models.model_database_handler.model_database_handler import save_instance, list_instances
from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Simulation.simulation_data.simulation_data import SimulationData
from Simulation.simulation_servicer.utils import update_today_data
from Utils.utils import convert_prices_to_np

ALGORITHMIC_MODELS_REL_PATH = "../models/algorithmic_models"
ALGORITHMIC_MODELS_ABS_PATH = "Models/models/algorithmic_models/"

MACHINE_LEARNING_MODELS_REL_PATH = "../models/machine_learning_models"
MACHINE_LEARNING_MODELS_ABS_PATH = "Models/models/machine_learning_models/"

DE = ModelDataEndpoint(DataProviderFrontend("[::]", 50051))

def convert_instance_into_univariate_model():
    pass

def create_composition_of_univariate_models():
    pass

def create_allocator_and_save_allocator():
    pass

def save_sel_instance():
    classes = list_model_classes_from_folder(ALGORITHMIC_MODELS_REL_PATH, ALGORITHMIC_MODELS_ABS_PATH)
    model_instance = ask_model_instance([e[0] for e in classes])
    parameters = ask_instance_parameters()
    new_instance = None
    for e in classes:
        if e[0] == model_instance:
            new_instance = e[1](*(tuple(parameters)))
            save_instance(e[0], new_instance)

def train_and_save_instance():
    classes = list_model_classes_from_folder(MACHINE_LEARNING_MODELS_REL_PATH, MACHINE_LEARNING_MODELS_ABS_PATH)
    model_instance = ask_model_instance([e[0] for e in classes])
    parameters = ask_instance_parameters()
    preprocessing_parameters = ask_preprocessing_parameters()
    new_instance = None
    for e in classes:
        if e[0] == model_instance:
            new_instance = e[1](*(tuple(parameters)))
            X, Y = new_instance.preprocessing(*(tuple(preprocessing_parameters + [DE])))
            new_instance.train(X, Y)
            save_instance(e[0], new_instance)

def test_instance():
    stock, start_date, end_date, pred_time, model_instance = ask_test_parameters(list_instances())

    data, target_data = model_instance.preprocessing(stock, start_date, end_date, pred_time, DE)

    predicted_values = model_instance.predict_on_batch(data)

    score = model_instance.evaluate(data, target_data)

    print("The loss function on the selected data corresponds to the following score {}".format(score))

    if ask_graph():
        render_graph(target_data, predicted_values)


def test_estimator():
    stock, start_date, end_date, pred_time, model_instance = ask_test_parameters(list_instances())

    dates, data, raw_prices, _ = DE.get_past_data([stock], ["dailyAdjusted", "cci", "adx", "ad", "aroon", "bbands", "ema", "macd", "obv", "rsi", "sma", "stoch"], start_date, end_date)
    current_data = {stock : SimulationData()}
    for daily_data in data:
        current_data = update_today_data(current_data, data[daily_data])
        model_instance.estimate(current_data)

    prices = convert_prices_to_np(raw_prices)[stock]
    prices = np.delete(prices, 0, axis=0)
    print(len(prices))
    estimations = np.array([estimation[stock] for estimation in model_instance.estimations])
    estimations = np.delete(estimations, estimations.shape[0]-1, axis=0)
    print(estimations.shape)

    render_graph(prices, estimations)


def stack_multiple_estimators():
    print("TO BE IMPLEMENTED")
