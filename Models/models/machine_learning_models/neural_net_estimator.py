"""import keras
import numpy as np

from Models.models.interfaces.estimator_interface import EstimatorInterface, record_estimation
from Utils.utils import convert_daily_data_to_np, convert_data_to_np, convert_prices_to_np
from sklearn import preprocessing
from Utils.utils import data_load
from keras.models import Model
from keras.layers import Dense, Dropout, Input, Activation
from keras import optimizers
from Models.model_database_handler.model_database_handler import *


class NeuralNetEstimator(EstimatorInterface):
    description = "Artificial Intelligence Approach using NeuralNets."

    model = None

    x_normalizer = None

    y_normalizer = None

    hyperparameters = None

    def __init__(self, buy_threshold, sell_threshold):
        self.set_threshold(buy_percentual_threshold=buy_threshold, sell_percentual_threshold=sell_threshold)

    def preprocessing(self, stock, start, end, pred_time):
        _, data_raw, prices_raw = data_load([stock], start, end)
        data = convert_data_to_np(data_raw)
        self.x_normalizer = preprocessing.MinMaxScaler()
        processed_data = self.x_normalizer.fit_transform(data[stock])
        X = np.array([processed_data[:][i].copy() for i in range(len(processed_data) - pred_time)])
        print(X.shape)

        prices = convert_prices_to_np(prices_raw)
        self.y_normalizer = preprocessing.MinMaxScaler()
        self.y_normalizer.fit(prices[stock])
        processed_prices = prices[stock]
        Y = np.array([processed_prices[:][i + pred_time].copy() for i in range(len(processed_prices) - pred_time)])
        print(Y.shape)
        return X, Y

    def train(self, X, Y):

        NNinput = Input(shape=(X.shape[1]), name='input')
        x = Dense(50, name='dense_0')(NNinput)
        x = Dropout(0.2, name='dropout_0')(x)
        x = Activation('relu', name='relu_0')(x)
        x = Dense(64, name='dense_1')(x)
        x = Dropout(0.2, name='dropout_1')(x)
        x = Activation('relu', name='relu_1')(x)
        x = Dense(50, name='dense_2')(x)
        x = Activation('relu', name='relu_2')(x)
        x = Dense(1, name='dense_3')(x)
        output = Activation('linear', name='linear_output')(x)

        self.model = Model(inputs=NNinput, outputs=output)
        adam = optimizers.Adam(lr=0.005)
        self.model.compile(optimizer=adam, loss='mse')
        self.model.fit(x=X, y=Y, batch_size=32, epochs=800, shuffle=True)

    @record_estimation
    def estimate(self, daily_data: dict) -> dict:
        estimations = {}
        vec = convert_daily_data_to_np(daily_data)
        for s in daily_data:
            estimations[s] = self.model.predict(self.x_normalizer.transform(vec[s].reshape(1, -1)))[0][0]
        return estimations

    def save_attributes(self):
        if self.model:
            self.model.save(PYTHON_PATH + "/instances/NeuralNetEstimator.h5")
            self.model = None

    def retrieve_attributes(self):
        if os.path.exists(PYTHON_PATH + "/instances/NeuralNetEstimator.h5"):
            self.model = keras.models.load_model(PYTHON_PATH + "/instances/NeuralNetEstimator.h5")


if __name__ == '__main__':
    model = NeuralNetEstimator(0.01, 0.0001)
    X, Y = model.preprocessing("GM", "2013-01-01", "2018-01-01", 1)
    model.train(X, Y)
    save_instance("NeuralNetEstimator", model)"""
