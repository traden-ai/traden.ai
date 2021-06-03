import numpy as np
import tensorflow as tf
import keras
import os

from constants import PYTHON_PATH
from models.estimator_interface import EstimatorInterface
from simulation.simulation import Simulation
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation
from keras import optimizers
from sklearn import preprocessing



class StackingEstimatorsInterface(EstimatorInterface):
    trainable_component = None

    x_normalizers = {}

    y_normalizers = {}

    def __init__(self, estimators, percentual_threshold=None, nominal_threshold=None):
        self.estimators = estimators
        self.set_threshold(percentual_threshold=percentual_threshold, nominal_threshold=nominal_threshold)
        self.set_threshold(percentual_threshold=percentual_threshold, nominal_threshold=nominal_threshold)
        self.x_normalizers = {}
        self.y_normalizers = {}

    def preprocessing(self, tradable_stocks: list, start_date: str, end_date: str, pred_time: int):
        raw_Y = []
        raw_X = []
        simul = None
        for estimator in self.estimators:
            estimator.reset_estimations()
            simul = Simulation(1, tradable_stocks, start_date, end_date, estimator)
            simul.execute()
            raw_X.append(estimator.get_estimations()[:-pred_time])
            estimator.reset_estimations()
        raw_Y = simul.prices
        X = convert_raw_to_x(raw_X)
        for stock in X:
            x_normalizer = preprocessing.MinMaxScaler()
            processed_data = x_normalizer.fit_transform(X[stock])
            X[stock] = np.array([processed_data[:][i].copy() for i in range(len(processed_data))])
            self.x_normalizers[stock] = x_normalizer
        Y = convert_raw_to_y(raw_Y, pred_time)
        for stock in Y:
            y_normalizer = preprocessing.MinMaxScaler()
            Y[stock] = y_normalizer.fit_transform(Y[stock].reshape(-1, 1))
            self.y_normalizers[stock] = y_normalizer
        return X, Y

    def train(self, X, Y):
        for ticker in X:
            if not self.trainable_component:
                NNet = Input(shape=(X[ticker].shape[1]), name='input')
                x = Dense(5, name='dense1')(NNet)
                x = Dense(1, name='dense2')(x)
                output = Activation('linear', name='linear_output')(x)

                self.trainable_component = Model(inputs=NNet, outputs=output)
                adam = optimizers.Adam(lr=0.01)
                self.trainable_component.compile(optimizer=adam, loss='mse')
                self.trainable_component.fit(x=X[ticker], y=Y[ticker], batch_size=32, epochs=150, shuffle=True)
            else:
                self.trainable_component.fit(x=X[ticker], y=Y[ticker], batch_size=32, epochs=150, shuffle=True)

    def estimate(self, daily_data: dict) -> dict:
        estimations = {}
        estimators_results = []
        for estimator in self.estimators:
            estimates = estimator.estimate(daily_data)
            estimators_results.append(estimates)
        for ticker in estimators_results[0]:
            daily_vec = np.array([estimate[ticker] for estimate in estimators_results])
            X = np.array(self.x_normalizers[ticker].transform(daily_vec.reshape(1, -1)))
            estimations[ticker] = float(self.y_normalizers[ticker].inverse_transform(self.trainable_component.predict(X))[0])
        return estimations

    def save_attributes(self):
        for estimator in self.estimators:
            estimator.save_attributes()
        if self.trainable_component:
            self.trainable_component.save(PYTHON_PATH + "/instances/TrainableComponent.h5")
            self.trainable_component = None

    def retrieve_attributes(self):
        for estimator in self.estimators:
            estimator.retrieve_attributes()
        if os.path.exists(PYTHON_PATH + "/instances/TrainableComponent.h5"):
            self.trainable_component = keras.models.load_model(PYTHON_PATH + "/instances/TrainableComponent.h5")


def convert_raw_to_x(raw_X):
    daily_model_estimates = {}
    for raw_model_data in raw_X:
        for iter in range(len(raw_model_data)):
            for ticker in raw_model_data[iter]:
                if ticker not in daily_model_estimates:
                    daily_model_estimates[ticker] = [[]] * len(raw_model_data)
                if not daily_model_estimates[ticker][iter]:
                    daily_model_estimates[ticker][iter] = [float(raw_model_data[iter][ticker])]
                else:
                    daily_model_estimates[ticker][iter].append(float(raw_model_data[iter][ticker]))
    for ticker in daily_model_estimates:
        daily_model_estimates[ticker] = np.array(daily_model_estimates[ticker])
    return daily_model_estimates


def convert_raw_to_y(raw_Y, pred_time):
    daily_prices = {}
    for ticker in raw_Y:
        daily_prices[ticker] = np.array(raw_Y[ticker][pred_time:])
    return daily_prices


if __name__ == '__main__':
    from model_database_handler.model_database_handler import get_instance, save_instance

    model1 = get_instance("NeuralNetEstimator")
    model2 = get_instance("FirstTradeModel")
    stacked = StackingEstimatorsInterface([model1, model2], percentual_threshold=0.01)
    X,Y = stacked.preprocessing(["GM"], "2013-01-01", "2018-01-01", 1)
    stacked.train(X, Y)
    save_instance("FirstStacked", stacked)
