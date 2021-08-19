import keras
import numpy as np

from DataProviderTester.main.data_provider_frontend import DataProviderFrontend
from Models.model_data_endpoint.model_data_endpoint import ModelDataEndpoint
from Models.models.interfaces.estimator_interface import EstimatorInterface, record_estimation
from utils.utils import convert_daily_data_to_np, convert_nominal_to_variation_2D
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

    def __init__(self, model_endpoint, buy_threshold, sell_threshold, time_steps):
        self.model_endpoint = model_endpoint
        self.set_threshold(buy_percentual_threshold=buy_threshold, sell_percentual_threshold=sell_threshold)
        self.time_steps = time_steps

    def preprocessing(self, stock, start, end, pred_time):
        data , self.x_dist = self.model_endpoint.get_percentile_variation_data_np([stock], ["dailyAdjusted", "cci", "adx", "ad", "aroon", "bbands", "ema", "macd", "obv", "rsi", "sma", "stoch"], start, end)
        X = []
        for i in range(self.time_steps, len(data[stock])-self.time_steps):
            X.append(data[stock][0, i - self.time_steps:i])
        X = np.array(X)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        print(X.shape)

        prices, self.y_dist = self.model_endpoint.get_percentile_variation_prices_np([stock], start, end)
        Y = []
        for i in range(self.time_steps, len(prices[stock]) - self.time_steps):
            Y.append(prices[stock][i, 0])
        Y = np.array(Y)
        print(Y.shape)
        return X, Y

    def train(self, X, Y):
        if self.model == None:
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
            adam = optimizers.Adam(lr=0.001)
            self.model.compile(optimizer=adam, loss='mse')
        self.model.fit(x=X, y=Y, batch_size=32, epochs=2000, shuffle=True)

    @record_estimation
    def estimate(self, daily_data) -> dict:
        estimations = {}
        vec = convert_daily_data_to_np(daily_data)
        if self.previous_vec:
            variations = {}
            for stock in vec:
                variation = np.array(convert_nominal_to_variation_2D([self.previous_vec[stock], vec[stock]]))
                variations[stock] = np.array(
                    [[self.x_dist[i].get_percentile(variation[0][i]) for i in range(len(variation[0]))]])
            self.past_vars.append(variations)
        self.previous_vec = vec
        if len(self.past_vars) > self.time_steps:
            self.past_vars = self.past_vars[1:]
        for s in daily_data:
            if len(self.past_vars) == self.time_steps:
                arr = np.array([self.past_vars[i][s].reshape(1,-1)[0] for i in range(len(self.past_vars))])
                arr = np.transpose(arr)
                arr = np.reshape(arr, (arr.shape[0], arr.shape[1], 1))
                nn_res = self.model.predict(arr)
                estimations[s] = float(self.y_dist.get_point(float(nn_res[0][0]))*daily_data[s].close)
            else:
                estimations[s] = getattr(daily_data[s], "close")
        return estimations

    def save_attributes(self):
        if self.model:
            self.model.save(PYTHON_PATH + "/instances/VariationLstmModel.h5")
            self.model = None

    def retrieve_attributes(self):
        if os.path.exists(PYTHON_PATH + "/instances/VariationLstmModel.h5"):
            self.model = keras.models.load_model(PYTHON_PATH + "/instances/VariationLstmModel.h5")


if __name__ == '__main__':
    model = VariationLstmModel(ModelDataEndpoint(DataProviderFrontend("[::]", "50051")), 0.01, 0.0001, 10)
    X, Y = model.preprocessing("MO", "2013-01-01", "2018-01-01", 1)
    model.train(X, Y)
    save_instance("VariationLstmModel", model)