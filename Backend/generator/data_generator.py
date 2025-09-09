from datetime import datetime

import yfinance as yf

from Backend.Licenta.Utils.Constants import Constants
from Backend.Licenta.Utils.database_connection import DatabaseConnection
from Backend.Licenta.Utils.trading_indicators import TradingIndicator


class DataGenerator:
    @staticmethod
    def get_statistics(stock_name, start_date, end_date):
        return yf.download(stock_name, start=start_date, end=end_date)

    @staticmethod
    def get_williams_indicator(data_frame):
        column = [0] * 13

        for i in range(14, len(data_frame) + 1):
            wpr = TradingIndicator.get_williams_indicator(data_frame.iloc[i - 14:i])
            column.append(wpr)

        data_frame['Williams'] = column
        return data_frame

    @staticmethod
    def get_relative_strength_index(data_frame):
        column = [0] * 13

        for i in range(14, len(data_frame) + 1):
            rsi = TradingIndicator.get_relative_strength_index(data_frame.iloc[i - 14:i])
            column.append(rsi)

        data_frame['RSI'] = column
        return data_frame

    @staticmethod
    def save_history_data_to_database(data_frame, stock_name, database_connection):
        values = []
        for index, row in data_frame.iterrows():
            values.append((stock_name, index.strftime('%Y-%m-%d'), row['Open'], row['Close'], row['High'], row['Low'], row['Williams'], row['RSI']))

        query = "INSERT INTO stock_data (stock_name, trading_date, open_price, close_price, high_price, low_price, williams_indicator, rsi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        with database_connection as cursor:
            cursor.executemany(query, values)


if __name__ == '__main__':
    db_connection = DatabaseConnection(Constants.HOST, Constants.USERNAME, Constants.PASSWORD, Constants.DATABASE)

    start_date = '2004-12-14'
    end_date = datetime.now().strftime("%Y-%m-%d")

    data_frame = DataGenerator.get_statistics('AAPL', start_date, end_date)
    data_frame = DataGenerator.get_williams_indicator(data_frame)
    data_frame = DataGenerator.get_relative_strength_index(data_frame)
    data_frame = data_frame.drop(data_frame.index[:13])
    DataGenerator.save_history_data_to_database(data_frame, 'AAPL', db_connection)

    data_frame = DataGenerator.get_statistics('GOOG', start_date, end_date)
    data_frame = DataGenerator.get_williams_indicator(data_frame)
    data_frame = DataGenerator.get_relative_strength_index(data_frame)
    data_frame = data_frame.drop(data_frame.index[:13])
    DataGenerator.save_history_data_to_database(data_frame, 'GOOG', db_connection)

    data_frame = DataGenerator.get_statistics('MSFT', start_date, end_date)
    data_frame = DataGenerator.get_williams_indicator(data_frame)
    data_frame = DataGenerator.get_relative_strength_index(data_frame)
    data_frame = data_frame.drop(data_frame.index[:13])
    DataGenerator.save_history_data_to_database(data_frame, 'MSFT', db_connection)

    data_frame = DataGenerator.get_statistics('AMZN', start_date, end_date)
    data_frame = DataGenerator.get_williams_indicator(data_frame)
    data_frame = DataGenerator.get_relative_strength_index(data_frame)
    data_frame = data_frame.drop(data_frame.index[:13])
    DataGenerator.save_history_data_to_database(data_frame, 'AMZN', db_connection)
