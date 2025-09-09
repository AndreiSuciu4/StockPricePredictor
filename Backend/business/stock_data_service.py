class StockDataService:
    def __init__(self, stock_data_repository):
        self.__stock_data_repository = stock_data_repository

    def add_stock_data(self, stock_data):
        self.__stock_data_repository.add_stock_data(stock_data)

    def get_history_data_for_certain_stock(self, stock_name):
        return self.__stock_data_repository.get_history_data_for_certain_stock(stock_name)

    def get_last_trading_date_for_stock(self, stock_name):
        return self.__stock_data_repository.get_last_trading_date_for_stock(stock_name)

    def get_nth_last_stock_record(self, stock_name, n):
        return self.__stock_data_repository.get_nth_last_stock_record(stock_name, n)
