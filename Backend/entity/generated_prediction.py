class GeneratedPrediction:
    def __init__(self, stock_name, user_email, last_date_for_stock, generated_date, generated_price, actual_price):
        self.__stock_name = stock_name
        self.__user_email = user_email
        self.__last_date_for_stock = last_date_for_stock
        self.__generated_date = generated_date
        self.__generated_price = generated_price
        self.__actual_price = actual_price

    def get_stock_name(self):
        return self.__stock_name

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    def get_user_email(self):
        return self.__user_email

    def set_user_email(self, user_email):
        self.__user_email = user_email

    def get_last_date_for_stock(self):
        return self.__last_date_for_stock

    def set_last_date_for_stock(self, last_date_for_stock):
        self.__last_date_for_stock = last_date_for_stock

    def get_generated_date(self):
        return self.__generated_date

    def set_generated_date(self, generated_date):
        self.__generated_date = generated_date

    def get_generated_price(self):
        return self.__generated_price

    def set_generated_price(self, generated_price):
        self.__generated_price = generated_price

    def get_actual_price(self):
        return self.__actual_price

    def set_actual_price(self, actual_price):
        self.__actual_price = actual_price

    def to_json(self):
        return {
            'stock_name': self.__stock_name,
            'user_email': self.__user_email,
            'last_date_for_stock': self.__last_date_for_stock,
            'generated_date': self.__generated_date,
            'generated_price': self.__generated_price,
            'actual_price': self.__actual_price
        }