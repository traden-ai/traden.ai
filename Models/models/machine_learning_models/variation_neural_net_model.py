import keras
import numpy as np

from Models.models.interfaces.estimator_interface import EstimatorInterface, record_estimation
from utils.data_distribution import convert_data_points_into_percentile_list, \
    convert_data_points_2D_into_percentile_2D
from utils.utils import convert_daily_data_to_np, convert_data_to_np, convert_prices_to_np, \
    convert_nominal_to_variation_1D, convert_nominal_to_variation_2D
from utils.utils import data_load
from keras.models import Model
from keras.layers import Dense, Dropout, Input, Activation
from keras import optimizers
from Models.model_database_handler.model_database_handler import *


class VariationNeuralNetModel(EstimatorInterface):
    description = "Artificial Intelligence Approach using NNs."

    model = None

    x_dist = None

    y_dist = None

    previous_vec = None

    def __init__(self, buy_threshold, sell_threshold):
        self.set_threshold(buy_percentual_threshold=buy_threshold, sell_percentual_threshold=sell_threshold)

    def preprocessing(self, stock, start, end, pred_time):
        _, data_raw, prices_raw = data_load([stock], start, end)
        data = convert_data_to_np(data_raw)
        data_variations = {}
        for stock in data:
            data_variations[stock] = np.array(convert_nominal_to_variation_2D(data[stock]))
        processed_data = data_variations[stock]
        processed_data, self.x_dist = convert_data_points_2D_into_percentile_2D(processed_data.transpose())
        transformed_data = np.array(processed_data).transpose()
        X_arr = np.array([list(transformed_data[:][i].copy()) for i in range(len(transformed_data) - pred_time)])
        X = np.array(X_arr)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        print(X.shape)

        prices = convert_prices_to_np(prices_raw)
        price_variations = {}
        for stock in prices:
            price_variations[stock] = np.array(convert_nominal_to_variation_1D(prices[stock]))
        processed_variations = price_variations[stock]
        Y_arr = [processed_variations[:][i + pred_time].copy() for i in range(len(processed_variations) - pred_time)]
        Y_arr, self.y_dist = convert_data_points_into_percentile_list(Y_arr)
        Y = np.array(Y_arr)
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
    def estimate(self, daily_data) -> dict:
        estimations = {}
        vec = convert_daily_data_to_np(daily_data)
        variations = {}
        if self.previous_vec:
            for stock in vec:
                variation = np.array(convert_nominal_to_variation_2D([self.previous_vec[stock], vec[stock]]))
                variations[stock] = np.array([[self.x_dist[i].get_percentile(variation[0][i]) for i in range(len(variation[0]))]])
        self.previous_vec = vec
        for s in daily_data:
            if s in variations:
                arr = variations[s]
                arr = np.reshape(arr, (arr.shape[0], arr.shape[1], 1))
                nn_res = self.model.predict(arr)
                estimations[s] = float(self.y_dist.get_point(float(nn_res[0][0]))*daily_data[s].close)
            else:
                estimations[s] = daily_data[s].close
        return estimations

    def save_attributes(self):
        if self.model:
            self.model.save(PYTHON_PATH + "/instances/VariationNeuralNetModel.h5")
            self.model = None

    def retrieve_attributes(self):
        if os.path.exists(PYTHON_PATH + "/instances/VariationNeuralNetModel.h5"):
            self.model = keras.models.load_model(PYTHON_PATH + "/instances/VariationNeuralNetModel.h5")


if __name__ == '__main__':
    model = VariationNeuralNetModel(0.01, 0.0001)
    X, Y = model.preprocessing("AMZN", "2013-01-01", "2018-01-01", 1)

    model.train(X, Y)
    save_instance("VariationNeuralNetModel", model)
