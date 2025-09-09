import threading
import time

import schedule
from datetime import date, timedelta

from Backend.Licenta.Generator.data_generator import DataGenerator
from Backend.Licenta.Utils.Constants import Constants
from Backend.Licenta.Utils.trading_indicators import TradingIndicator
from Backend.Licenta.entity.stock_data import StockData


class Job:
    def __init__(self, stock_data_service, generated_prediction_service, apple_model, google_model, amazon_model, microsoft_model):
        self.__stock_data_service = stock_data_service
        self.__generate_prediction_service = generated_prediction_service
        self.__apple_model = apple_model
        self.__google_model = google_model
        self.__amazon_model = amazon_model
        self.__microsoft_model = microsoft_model

    def add_history_data(self):
        stock_names = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
        end_date = date.today()
        start_date = end_date - timedelta(days=25)

        for stock_name in stock_names:
            data_frame = DataGenerator.get_statistics(stock_name, start_date, end_date)
            yesterday = end_date - timedelta(days=1)

            if data_frame.index[-1].strftime("%Y-%m-%d") != yesterday.strftime("%Y-%m-%d"):
                return

            last_trading_date_from_db = self.__stock_data_service.get_last_trading_date_for_stock(stock_name)

            if yesterday.strftime("%Y-%m-%d") != last_trading_date_from_db:
                data_frame = data_frame.tail(14)
                wpr = TradingIndicator.get_williams_indicator(data_frame)
                rsi = TradingIndicator.get_relative_strength_index(data_frame)

                data_frame = data_frame.tail(1)

                stock_data = StockData(stock_name, data_frame.index[0].strftime("%Y-%m-%d"), data_frame['Open'][0],
                                       data_frame['Close'][0], data_frame['High'][0], data_frame['Low'][0], wpr, rsi)
                self.__stock_data_service.add_stock_data(stock_data)

    def add_actual_price(self):
        stock_names = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
        end_date = date.today()
        start_date = end_date - timedelta(days=25)

        for stock_name in stock_names:
            data_frame = DataGenerator.get_statistics(stock_name, start_date, end_date)
            self.__generate_prediction_service.update_actual_price(stock_name, data_frame.index[-7].strftime("%Y-%m-%d"), data_frame['Close'][-7])

    def contiune_learning(self):
        history_data = self.__stock_data_service.get_nth_last_stock_record('AAPL', 90 + Constants.LOOK_BACK)
        self.__apple_model.contiune_learning(history_data)

        history_data = self.__stock_data_service.get_nth_last_stock_record('GOOG', 90 + Constants.LOOK_BACK)
        self.__google_model.contiune_learning(history_data)

        history_data = self.__stock_data_service.get_nth_last_stock_record('AMZN', 90 + Constants.LOOK_BACK)
        self.__amazon_model.contiune_learning(history_data)

        history_data = self.__stock_data_service.get_nth_last_stock_record('MSFT', 90 + Constants.LOOK_BACK)
        self.__microsoft_model.contiune_learning(history_data)

    def define_jobs(self):
        schedule.every().day.at("04:00").do(self.add_history_data)
        schedule.every().day.at("04:00").do(self.add_actual_price)
        schedule.every(110).days.do(self.contiune_learning)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_jobs(self):
        job_thread = threading.Thread(target=self.define_jobs)
        job_thread.start()
