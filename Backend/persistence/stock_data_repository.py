from Backend.Licenta.entity.stock_data import StockData


class StockDataRepository:
    def __init__(self, database_connection):
        self._db_connection = database_connection

    def add_stock_data(self, stock_data):
        query = "INSERT INTO stock_data (stock_name, trading_date, open_price, close_price, high_price, low_price, williams_indicator, rsi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (stock_data.get_stock_name(), stock_data.get_trading_date(), stock_data.get_open_price(), stock_data.get_close_price(), stock_data.get_high_price(), stock_data.get_low_price(), stock_data.get_williams_indicator(), stock_data.get_rsi())

        with self._db_connection as cursor:
            cursor.execute_query(query, values)

    def get_last_trading_date_for_stock(self, stock_name):
        query = "SELECT trading_date FROM stock_data WHERE stock_name = %s ORDER BY id DESC LIMIT 1"
        values = (stock_name,)

        with self._db_connection as cursor:
            result = cursor.fetch_one(query, values)

            if result is None:
                return None
            else:
                return result[0]

    def get_nth_last_trading_date(self, stock_name, n):
        query = "SELECT trading_date FROM stock_data WHERE stock_name = %s ORDER BY id DESC LIMIT 1 OFFSET %s;"
        values = (stock_name, n)

        with self._db_connection as cursor:
            result = cursor.fetch_one(query, values)

            if result is None:
                return None
            else:
                return result[0]

    def get_history_data_for_certain_stock(self, stock_name):
        query = "SELECT * FROM stock_data WHERE stock_name = %s"
        values = (stock_name, )

        with self._db_connection as cursor:
            results = cursor.fetch_all(query, values)

            if results is None:
                return None
            else:
                stock_data = []
                for result in results:
                    stock_data.append(
                        StockData(result[1], result[2], result[3], result[4], result[7], result[8], result[5], result[6]))
                return stock_data

    def get_nth_last_stock_record(self, stock_name, n):
        query = "SELECT * FROM stock_data WHERE stock_name = %s ORDER BY id DESC LIMIT %s"
        values = (stock_name, n)

        with self._db_connection as cursor:
            results = cursor.fetch_all(query, values)

            if results is None:
                return None
            else:
                stock_data = []
                for result in results:
                    stock_data.append(
                        StockData(result[1], result[2], result[3], result[4], result[7], result[8], result[5],
                                  result[6]))
                return stock_data
