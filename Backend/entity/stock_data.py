class StockData:
    def __init__(self, stock_name, trading_date, open_price, close_price, high_price, low_price, williams_indicator, rsi):
        self.__stock_name = stock_name
        self.__trading_date = trading_date
        self.__open_price = open_price
        self.__close_price = close_price
        self.__high_price = high_price
        self.__low_price = low_price
        self.__williams_indicator = williams_indicator
        self._rsi = rsi

    def get_stock_name(self):
        return self.__stock_name

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    def get_trading_date(self):
        return self.__trading_date

    def set_trading_date(self, trading_date):
        self.__trading_date = trading_date

    def get_open_price(self):
        return self.__open_price

    def set_open_price(self, open_price):
        self.__open_price = open_price

    def get_close_price(self):
        return self.__close_price

    def set_close_price(self, close_price):
        self.__close_price = close_price

    def get_high_price(self):
        return self.__high_price

    def set_high_price(self, high_price):
        self.__high_price = high_price

    def get_low_price(self):
        return self.__low_price

    def set_low_price(self, low_price):
        self.__low_price = low_price

    def get_williams_indicator(self):
        return self.__williams_indicator

    def set_williams_indicator(self, williams):
        self.__williams_indicator = williams

    def get_rsi(self):
        return self._rsi

    def set_rsi(self, rsi):
        self._rsi = rsi

    def to_json(self):
        return {
            "stock_name": self.__stock_name,
            "trading_date": self.__trading_date,
            "open_price": self.__open_price,
            "close_price": self.__close_price,
            "high_price": self.__high_price,
            "low_price": self.__low_price,
            "williams_indicator": self.__williams_indicator,
            "rsi": self._rsi
        }
