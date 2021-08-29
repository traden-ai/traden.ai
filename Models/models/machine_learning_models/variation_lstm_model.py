import keras
import numpy as np
import tensorflow as tf

from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Models.model_data_endpoint.model_data_endpoint import ModelDataEndpoint
from Models.models.interfaces.estimator_interface import EstimatorInterface, record_estimation
from Utils.utils import convert_daily_data_to_np, convert_nominal_to_variation_2D, convert_daily_simulation_data_to_np
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation
from keras import optimizers
from Models.model_database_handler.model_database_handler import *


class VariationLstmModel(EstimatorInterface):
    description = "Artificial Intelligence Approach using LSTMs."

    model = None

    x_dist = None

    y_dist = None

    previous_vec = None

    past_vars = []

    time_steps = None

    model_endpoint = None

    def __init__(self, buy_threshold, sell_threshold, time_steps):
        self.set_threshold(buy_percentual_threshold=float(buy_threshold), sell_percentual_threshold=float(sell_threshold))
        self.time_steps = int(time_steps)

    def preprocessing(self, stock, start, end, pred_time, data_endpoint):
        if not self.x_dist:
            raw_data , self.x_dist = data_endpoint.get_percentile_variation_data_np([stock], ["dailyAdjusted", "cci", "adx", "ad", "aroon", "bbands", "ema", "macd", "obv", "rsi", "sma", "stoch"], start, end)
        else:
            raw_data, _ = data_endpoint.get_percentile_variation_data_np([stock],["dailyAdjusted", "cci", "adx", "ad",
                                                                                    "aroon", "bbands", "ema", "macd",
                                                                                    "obv", "rsi", "sma", "stoch"],
                                                                                   start, end)

        data = np.delete(raw_data[stock], raw_data[stock].shape[1] - 1, axis=1)
        print(data.shape)
        X = []
        for i in range(self.time_steps, data.shape[1] - self.time_steps):
            X.append(data[:, i - self.time_steps:i])
        X = np.array(X)
        X = np.reshape(X, (X.shape[0], X.shape[2], X.shape[1]))
        print(X.shape)

        if not self.y_dist:
            raw_prices, self.y_dist = data_endpoint.get_percentile_variation_prices_np([stock], start, end)
        else:
            raw_prices, _ = data_endpoint.get_percentile_variation_prices_np([stock], start, end)
        prices = np.delete(raw_prices[stock], 0, axis=1)
        Y = []
        for i in range(self.time_steps, prices.shape[1] - self.time_steps):
            Y.append(prices[0, i])
        Y = np.array(Y)
        print(Y.shape)
        return X, Y

    def train(self, X, Y):
        if self.model == None:
            NNinput = Input(shape=(X.shape[1], X.shape[2]), name='input')
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
            adam = optimizers.Adam(lr=0.001)
            self.model.compile(optimizer=adam, loss='mse')
        self.model.fit(x=X, y=Y, batch_size=32, epochs=100, shuffle=True)

    def predict_on_batch(self, X):
        return self.model.predict_on_batch(X)

    def evaluate(self, X, Y):
        score = self.model.evaluate(X, Y)
        return score

    @record_estimation
    def estimate(self, daily_data) -> dict:
        estimations = {}
        vec = convert_daily_simulation_data_to_np(daily_data, attributes=["dailyAdjusted", "cci", "adx", "ad",
                                                                                    "aroon", "bbands", "ema", "macd",
                                                                                    "obv", "rsi", "sma", "stoch"])
        if self.previous_vec:
            variations = {}
            for stock in vec:
                input = np.array([self.previous_vec[stock], vec[stock]]).transpose()
                variation = np.array(convert_nominal_to_variation_2D(input))
                variations[stock] = np.array(
                    [[self.x_dist[stock][i].get_percentile(variation[i][0]) for i in range(len(variation))]])
            self.past_vars.append(variations)
        self.previous_vec = vec
        if len(self.past_vars) > self.time_steps:
            self.past_vars = self.past_vars[1:]
        for s in daily_data:
            if len(self.past_vars) == self.time_steps:
                arr = np.stack([self.past_vars[i][s] for i in range(len(self.past_vars))])
                arr = np.reshape(arr, (arr.shape[1], arr.shape[0], arr.shape[2]))
                nn_res = self.model.predict(arr)
                estimations[s] = float(self.y_dist[s].get_point(float(nn_res[0][0]))[0]*daily_data[s].dailyAdjusted.adjustedClose)
            else:
                estimations[s] = daily_data[s].dailyAdjusted.adjustedClose
        return estimations

    def save_attributes(self):
        if self.model:
            self.model.save(PYTHON_PATH + "/instances/VariationLstmModel.h5")
            self.model = None

    def retrieve_attributes(self):
        if os.path.exists(PYTHON_PATH + "/instances/VariationLstmModel.h5"):
            self.model = keras.models.load_model(PYTHON_PATH + "/instances/VariationLstmModel.h5")


def my_loss_fn(y_true, y_pred):
    squared_difference = tf.square(y_true - y_pred)
    return tf.reduce_mean(squared_difference, axis=-1)

def special_loss_fn(y_true, y_pred):
    squared_difference = tf.square(y_true - y_pred)
    correction_term = 0.1/(20*(tf.square(0.5 - y_pred)) + 0.5)
    return tf.reduce_mean(squared_difference + correction_term, axis=-1)

if __name__ == '__main__':
    import random

    model = VariationLstmModel( 0.01, 0.0001, 10)
    X, Y = model.preprocessing("MO", "2001-01-01", "2018-01-01", 1, ModelDataEndpoint(DataProviderFrontend("[::]", "50051")))
    model.train(X, Y)
    X, Y = model.preprocessing("MO", "2018-01-01", "2020-01-01", 1,
                               ModelDataEndpoint(DataProviderFrontend("[::]", "50051")))
    lst = []
    for i in range(Y.shape[0]):
        lst.append(random.uniform(0, 1))
    print(my_loss_fn(Y, np.array(lst)))

    predictions = model.model.predict_on_batch(X).reshape(-1)
    print(predictions)
    results = []
    print(float(my_loss_fn(Y, predictions)))
    for i in range(1000):
        print("---------------------------------------------------------------")
        np.random.shuffle(predictions)
        results.append(float(my_loss_fn(Y, predictions)))
    results.sort()
    print(results)
    my_result = model.evaluate(X, Y)
    for i in range(len(results)):
        if results[i] >= my_result:
            print(" The result is in the percentile {}".format(i))
            break

    X, Y = model.preprocessing("MO", "2020-01-01", "2021-01-01", 1,
                               ModelDataEndpoint(DataProviderFrontend("[::]", "50051")))
    lst = []
    for i in range(Y.shape[0]):
        lst.append(random.uniform(0, 1))
    print(my_loss_fn(Y, np.array(lst)))

    predictions = model.model.predict_on_batch(X).reshape(-1)
    print(predictions)
    results = []
    print(float(my_loss_fn(Y, predictions)))
    for i in range(1000):
        print("---------------------------------------------------------------")
        np.random.shuffle(predictions)
        results.append(float(my_loss_fn(Y, predictions)))
    results.sort()
    print(results)
    my_result = model.evaluate(X, Y)
    for i in range(len(results)):
        if results[i] >= my_result:
            print(" The result is in the percentile {}".format(i))
            break

    save_instance("VariationLstmModel", model)