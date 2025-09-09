from Backend.Licenta.entity.generated_prediction import GeneratedPrediction


class GeneratedPredictionRepository:
    def __init__(self, database_connection):
        self._db_connection = database_connection

    def add_generated_prediction(self, generated_prediction):
        query = "INSERT INTO generated_prediction (stock_name, user_email, last_date_for_stock, generated_date, generated_price, actual_price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (generated_prediction.get_stock_name(), generated_prediction.get_user_email(), generated_prediction.get_last_date_for_stock(), generated_prediction.get_generated_date(), generated_prediction.get_generated_price(),
                  generated_prediction.get_actual_price())

        with self._db_connection as cursor:
            try:
                cursor.execute_query(query, values)
            except Exception as _:
                pass

    def update_actual_price(self, stock_name, last_date_for_stock, actual_price):
        query = "UPDATE generated_prediction SET actual_price = %s WHERE stock_name = %s AND last_date_for_stock = %s"
        values = (actual_price, stock_name, last_date_for_stock)

        with self._db_connection as cursor:
            cursor.execute_query(query, values)

    def get_generated_prediction_by_email_and_last_date(self, user_email, last_date):
        query = "SELECT * FROM generated_prediction WHERE user_email = %s AND last_date_for_stock = %s"
        values = (user_email, last_date)

        with self._db_connection as cursor:
            results = cursor.fetch_all(query, values)

            if results is None:
                return None
            else:
                generated_predictions = []
                for result in results:
                    generated_predictions.append(GeneratedPrediction(result[1], result[2], result[3], result[6], result[4], result[5]))
                return generated_predictions
