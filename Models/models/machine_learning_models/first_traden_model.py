import random

from Models.model_database_handler.model_database_handler import save_instance
from constants import PYTHON_PATH
from models.estimator_interface import EstimatorInterface, record_estimation
from models.model_interface import *
from utils.utils import convert_daily_data_to_np, convert_data_to_np, convert_prices_to_np
from sklearn import preprocessing
from utils.utils import data_load
import keras
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation
from keras import optimizers
import numpy as np
import os
from model_database_handler.model_database_handler import *


class FirstTradenModel(EstimatorInterface):
    description = "Artificial Intelligence Approach using LSTMs."

    model = None

    x_normalizer = None

    y_normalizer = None

    past_vecs = []

    time_steps = None

    def __init__(self, buy_threshold, sell_threshold, time_steps):
        self.set_threshold(buy_percentual_threshold=buy_threshold, sell_percentual_threshold=sell_threshold)
        self.time_steps = time_steps

    def preprocessing(self, stock, start, end, pred_time):
        _, data_raw, prices_raw = data_load([stock], start, end)
        data = convert_data_to_np(data_raw)
        self.x_normalizer = preprocessing.MinMaxScaler()
        processed_data = self.x_normalizer.fit_transform(data[stock])
        X_arr = np.array([list(processed_data[:][i].copy()) for i in range(len(processed_data) - pred_time)])
        X = []
        for i in range(self.time_steps, len(X_arr)-self.time_steps):
            X.append(X_arr[i - self.time_steps:i, 0])
        X = np.array(X)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        print(X.shape)

        prices = convert_prices_to_np(prices_raw)
        self.y_normalizer = preprocessing.MinMaxScaler()
        self.y_normalizer.fit(prices[stock])
        processed_prices = prices[stock]
        Y_arr = np.array([processed_prices[:][i + pred_time].copy() for i in range(len(processed_prices) - pred_time)])
        Y = []
        for i in range(self.time_steps, len(Y_arr) - self.time_steps):
            Y.append(Y_arr[i, 0])
        Y = np.array(Y)
        print(Y.shape)
        return X, Y

    def train(self, X, Y):

        NNinput = Input(shape=(X.shape[1], 1), name='input')
        x = LSTM(50, name='lstm_0', return_sequences=True)(NNinput)
        x = Dropout(0.2, name='dropout_0')(x)
        x = Activation('relu', name='relu_0')(x)
        x = LSTM(64, name='dense_1')(x)
        x = Dropout(0.2, name='dropout_1')(x)
        x = Activation('relu', name='relu_1')(x)
        x = Dense(50, name='dense_2')(x)
        x = Activation('relu', name='relu_2')(x)
        x = Dense(1, name='dense_3')(x)
        output = Activation('linear', name='linear_output')(x)

        self.model = Model(inputs=NNinput, outputs=output)
        adam = optimizers.Adam(lr=0.005)
        self.model.compile(optimizer=adam, loss='mse')
        self.model.fit(x=X, y=Y, batch_size=32, epochs=400, shuffle=True)

    @record_estimation
    def estimate(self, daily_data) -> dict:
        estimations = {}
        vec = convert_daily_data_to_np(daily_data)
        self.past_vecs.append(vec)
        if len(self.past_vecs) > self.time_steps:
            self.past_vecs = self.past_vecs[1:]
        for s in daily_data:
            if len(self.past_vecs) == self.time_steps:
                arr = np.array([self.x_normalizer.transform(self.past_vecs[i][s].reshape(1,-1))[0] for i in range(len(self.past_vecs))])
                arr = np.transpose(arr)
                arr = np.reshape(arr, (arr.shape[0], arr.shape[1], 1))
                estimations[s] = self.model.predict(arr)[0][0]
            else:
                estimations[s] = getattr(daily_data[s], "close")
        return estimations

    def save_attributes(self):
        if self.model:
            self.model.save(PYTHON_PATH + "/instances/FirstTradenModel.h5")
            self.model = None

    def retrieve_attributes(self):
        if os.path.exists(PYTHON_PATH + "/instances/FirstTradenModel.h5"):
            self.model = keras.models.load_model(PYTHON_PATH + "/instances/FirstTradenModel.h5")


if __name__ == '__main__':
    model = FirstTradenModel(0.01, 0.0001, 5)
    X, Y = model.preprocessing("GM", "2013-01-01", "2018-01-01", 1)
    model.train(X, Y)
    save_instance("FirstTradenModel", model)
