from Backend.Licenta.Utils.Constants import Constants


class StockService:
    def __init__(self, stock_data_repository, apple_model, amazon_model, google_model, microsoft_model):
        self.__stock_data_repository = stock_data_repository
        self.__apple_model = apple_model
        self.__amazon_model = amazon_model
        self.__google_model = google_model
        self.__microsoft_model = microsoft_model

    def predict_price(self, stock_name):
        input_data = self.__stock_data_repository.get_nth_last_stock_record(stock_name, Constants.LOOK_BACK)
        predicted_value = 0
        if stock_name == 'AAPL':
            predicted_value = self.__apple_model.generate_prediction(input_data)
        elif stock_name == 'AMZN':
            predicted_value = self.__amazon_model.generate_prediction(input_data)
        elif stock_name == 'GOOG':
            predicted_value = self.__google_model.generate_prediction(input_data)
        elif stock_name == 'MSFT':
            predicted_value = self.__microsoft_model.generate_prediction(input_data)

        return predicted_value

