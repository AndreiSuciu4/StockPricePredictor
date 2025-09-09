from Backend.Licenta.entity.generated_prediction import GeneratedPrediction
from datetime import datetime


class GeneratedPredictionService:
    def __init__(self, generated_prediction_repository, stock_data_repository):
        self.__generated_prediction_repository = generated_prediction_repository
        self.__stock_data_repository = stock_data_repository

    def add_generated_prediction(self, stock_name, current_user, generated_price, actual_price):
        last_date_for_stock = self.__stock_data_repository.get_last_trading_date_for_stock(stock_name)
        current_date = datetime.now().strftime("%Y-%m-%d")

        generated_prediction = GeneratedPrediction(stock_name, current_user.get_email(), last_date_for_stock, current_date, generated_price, actual_price)
        self.__generated_prediction_repository.add_generated_prediction(generated_prediction)

    def update_actual_price(self, stock_name, date, actual_price):
        self.__generated_prediction_repository.update_actual_price(stock_name, date, actual_price)

    def get_generated_prediction_by_email_and_last_date(self, user_email):
        last_date_for_stock = self.__stock_data_repository.get_nth_last_trading_date('AAPL', 6)
        return self.__generated_prediction_repository.get_generated_prediction_by_email_and_last_date(user_email, last_date_for_stock)

