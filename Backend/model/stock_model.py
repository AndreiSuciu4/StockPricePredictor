from datetime import datetime
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam
from keras.layers import Dropout
from tensorflow.python.ops.init_ops_v2 import he_uniform
from keras.metrics import MeanSquaredError, MeanAbsoluteError, MeanAbsolutePercentageError

from Backend.Licenta.Utils.Constants import Constants
from Backend.Licenta.Utils.database_connection import DatabaseConnection
from Backend.Licenta.repository.stock_data_repository import StockDataRepository


class StockModel:
    def __init__(self):
        self.__stock_data = []
        self.__converted_data = []
        self.__close_price = []
        self.__trading_dates = []
        self.__scaled_data = []
        self.__x_train = []
        self.__y_train = []
        self.__model = Sequential()

    def set_stock_data(self, stock_data):
        self.__stock_data = stock_data

    def buid_and_train_model(self):
        self.__convert_data()
        self.__scale_data()
        self.__generate_train_data()
        self.__build_model()

    def __convert_data(self):
        for row in self.__stock_data:
            converted_row = [row.get_open_price(), row.get_close_price(), row.get_williams_indicator(), row.get_rsi()]
            self.__converted_data.append(converted_row)
            self.__close_price.append(row.get_close_price())
            self.__trading_dates.append(row.get_trading_date())

        self.__converted_data = np.asarray(self.__converted_data)
        self.__close_price = np.asarray(self.__close_price)

    def __generate_train_data(self):
        test_data_length = int(len(self.__stock_data) * 0.9)
        windows_no = Constants.WINDOWS_NO
        window_size = int(test_data_length / windows_no)
        look_back = Constants.LOOK_BACK
        no_days = Constants.NO_DAYS

        for i in range(windows_no):
            for j in range(i * window_size, window_size * (i + 1) - look_back - no_days):
                row_train = []
                for k in range(look_back - 1, -1, -1):
                    row_train.append(self.__scaled_data_attribute[j + k])
                self.__x_train.append(row_train)
                self.__y_train.append(self.__scaled_data_output[j + look_back + no_days])

        self.__x_train = np.asarray(self.__x_train)
        self.__y_train = np.asarray(self.__y_train)

    def __scale_data(self):
        test_data_length = int(len(self.__stock_data) * 0.9)
        windows_no = Constants.WINDOWS_NO
        window_size = int(test_data_length / windows_no)

        self.__min_max_scaler_attribute = MinMaxScaler(feature_range=(0, 1))
        self.__min_max_scaler_output = MinMaxScaler(feature_range=(0, 1))

        self.__scaled_data_attribute = []
        self.__scaled_data_output = []

        close_price = self.__close_price.reshape(-1, 1)

        for index in range(0, test_data_length - window_size, window_size):
            self.__scaled_data_attribute.append(
                self.__min_max_scaler_attribute.fit_transform(self.__converted_data[index:index + window_size]))

            self.__scaled_data_output.append(
                self.__min_max_scaler_output.fit_transform(close_price[index:index + window_size]))

        self.__scaled_data_attribute.append(
            self.__min_max_scaler_attribute.fit_transform(self.__converted_data[index + window_size:]))

        self.__scaled_data_output.append(
            self.__min_max_scaler_output.fit_transform(close_price[index + window_size:]))

        self.__scaled_data_attribute = np.concatenate(self.__scaled_data_attribute, axis=0)
        self.__scaled_data_attribute = np.squeeze(self.__scaled_data_attribute)

        self.__scaled_data_output = np.concatenate(self.__scaled_data_output, axis=0)
        self.__scaled_data_output = np.squeeze(self.__scaled_data_output)

    def __build_model(self):
        self.__model.add(
            LSTM(units=64, return_sequences=True, input_shape=(self.__x_train.shape[1], self.__x_train.shape[2])))
        self.__model.add(Dropout(0.3))

        self.__model.add(LSTM(units=128, activation='tanh'))
        self.__model.add(Dropout(0.3))

        self.__model.add(Dense(units=256, activation='tanh', kernel_initializer=he_uniform()))
        self.__model.add(Dropout(0.3))

        self.__model.add(Dense(units=128, activation='tanh', kernel_initializer=he_uniform()))
        self.__model.add(Dropout(0.3))

        self.__model.add(Dense(units=1))

        self.__model.compile(optimizer=Adam(), loss='mse', metrics=['mae'])

        self.__model.fit(self.__x_train, self.__y_train, epochs=Constants.EPOCHS_NO)

    def generate_prediction(self, input_data):
        converted_data = self.__convert_input_data(input_data)

        converted_data = self.__min_max_scaler_attribute.transform(converted_data)
        converted_data = np.reshape(converted_data, (-1, Constants.LOOK_BACK, Constants.FEATURES_NO))

        prediction = self.__model.predict(converted_data)
        prediction = self.__min_max_scaler_output.inverse_transform(prediction)
        prediction = prediction.astype(np.float64)
        return prediction[0][0]

    @staticmethod
    def __convert_input_data(input_data):
        converted_data = []
        for row in input_data:
            converted_row = [row.get_open_price(), row.get_close_price(), row.get_williams_indicator(),
                             row.get_rsi()]
            converted_data.append(converted_row)

        converted_data = np.asarray(converted_data)
        return converted_data

    def contiune_learning(self, input_data):
        converted_data = self.__convert_input_data(input_data)
        min_max_scaler_attributes = MinMaxScaler(feature_range=(0, 1))

        scaled_data = min_max_scaler_attributes.fit_transform(converted_data)
        lock_back = Constants.LOOK_BACK
        no_days = Constants.NO_DAYS

        x_train = []
        y_train = []

        for i in range(0, len(scaled_data) - lock_back - no_days):
            row_train = []
            for j in range(lock_back):
                row_train.append(self.__scaled_data_attribute[i + j])
            x_train.append(row_train)
            y_train.append(self.__scaled_data_output[i - 1 + lock_back + no_days])

        x_train = np.asarray(x_train)
        y_train = np.asarray(y_train)

        self.__model.fit(x_train, y_train, epochs=Constants.EPOCHS_NO)

    def get_test_data(self):
        data_length = len(self.__stock_data)
        train_data_length = int(data_length * 0.9)

        look_back = Constants.LOOK_BACK
        no_days = Constants.NO_DAYS

        x_test = []
        y_test = []
        trading_date_test = []

        for i in range(train_data_length, data_length - look_back - no_days):
            row_test = []
            for j in range(look_back - 1, -1, -1):
                row_test.append(self.__scaled_data_attribute[i + j])
            x_test.append(row_test)
            y_test.append(self.__close_price[i + look_back + no_days])
            trading_date_test.append(self.__trading_dates[i + look_back + no_days])

        x_test = np.asarray(x_test)
        y_test = np.asarray(y_test)
        return x_test, y_test, trading_date_test

    def generate_prediction_test(self, input):
        lock_back = Constants.LOOK_BACK
        features_no = Constants.FEATURES_NO

        input = np.reshape(input, (-1, lock_back, features_no))
        prediction = self.__model.predict(input)
        prediction = self.__min_max_scaler_output.inverse_transform(prediction)
        return prediction

    def generate_error(self, predictions, targets):
        mse = MeanSquaredError()
        mse.update_state(predictions, targets)

        mae = MeanAbsoluteError()
        mae.update_state(predictions, targets)

        mape = MeanAbsolutePercentageError()
        mape.update_state(predictions, targets)
        return mse.result().numpy(), mae.result().numpy(), mape.result().numpy()

    @staticmethod
    def print_prediction(y, pred, trading_dates):
        date = [datetime.strptime(d, '%Y-%m-%d') for d in trading_dates]
        fig, ax = plt.subplots(figsize=(24, 12))
        ax.plot(date, y, color='blue', label='Actual price')
        ax.plot(date, pred, color='red', label='Predicted price')

        months = mdates.MonthLocator()  # new
        ax.xaxis.set_major_locator(months)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.title('Close price prediction')
        plt.xlabel('Trading date')
        plt.ylabel('Close price USD')
        plt.legend(['Actual price', 'Predicted price'], loc='upper left', fontsize=12)
        plt.show()


if __name__ == '__main__':
    db_connection = DatabaseConnection(Constants.HOST, Constants.USERNAME, Constants.PASSWORD, Constants.DATABASE)
    stock_data_repository = StockDataRepository(db_connection)
    stock_model = StockModel()
    stock_model.set_stock_data(stock_data_repository.get_history_data_for_certain_stock('AMZN'))
    stock_model.buid_and_train_model()
    x_test, y_test, trading_dates = stock_model.get_test_data()
    prediction = stock_model.generate_prediction_test(x_test)
    mse, mae, mape = stock_model.generate_error(prediction, y_test)
    print("MSE = " + str(mse) + " MAE = " + str(mae) + " MAPE = " + str(mape))
    stock_model.print_prediction(y_test, prediction, trading_dates)
