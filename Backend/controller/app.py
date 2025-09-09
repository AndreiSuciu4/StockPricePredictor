import json
from functools import wraps

from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
import jwt
import datetime

from Backend.Licenta.Model.stock_model import StockModel
from Backend.Licenta.Service.generated_prediction_service import GeneratedPredictionService
from Backend.Licenta.Service.stock_data_service import StockDataService
from Backend.Licenta.Service.stock_model_service import StockService
from Backend.Licenta.Service.user_service import UserService
from Backend.Licenta.Utils.Constants import Constants
from Backend.Licenta.Utils.database_connection import DatabaseConnection
from Backend.Licenta.jobs.job import Job
from Backend.Licenta.repository.generated_prediction_repository import GeneratedPredictionRepository
from Backend.Licenta.repository.stock_data_repository import StockDataRepository
from Backend.Licenta.repository.user_repository import UserRepository


class StockController:
    def __init__(self, app, stock_model_service, stock_data_service, user_service, generated_prediction_service):
        self.__app = app
        self.__register_routes()
        self.__stock_service = stock_model_service
        self.__stock_data_service = stock_data_service
        self.__user_service = user_service
        self.__generated_prediction_service = generated_prediction_service

    def token_required(self, function):
        @wraps(function)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, self.__app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = user_service.find_user_by_email(data["email"])
            except Exception as ex:
                return jsonify({'message': str(ex)}), 401

            return function(current_user, *args, **kwargs)

        return decorated

    def __register_routes(self):
        @self.__app.route('/stock-prediction')
        @self.token_required
        def predict_price(current_user):
            stock = request.args.get('stock')
            prediction = self.__stock_service.predict_price(stock)
            self.__generated_prediction_service.add_generated_prediction(stock, current_user, float(prediction), 0)
            return jsonify({'prediction': prediction})

        @app.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            email = data['email']
            password = data['password']

            try:
                user = self.__user_service.login(email, password)
                generated_predictions_notification = self.__generated_prediction_service.get_generated_prediction_by_email_and_last_date(email)
                json_predictions = [p.to_json() for p in generated_predictions_notification]
                json_predictions_str = json.dumps(json_predictions)

                token = jwt.encode(
                    {'email': email, 'firstname': user.get_firstname(), 'lastname': user.get_lastname(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                    self.__app.config['SECRET_KEY'])
                return jsonify({'token': token, 'generated_predictions': json_predictions_str})
            except Exception as _:
                return make_response('Invalid data!', 401)

        @app.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            firstname = data['firstName']
            lastname = data['lastName']
            email = data['email']
            password = data['password']

            try:
                self.__user_service.register(firstname, lastname, email, password)
                token = jwt.encode(
                    {'email': email, 'firstname': firstname, 'lastname': lastname, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                    self.__app.config['SECRET_KEY'])
                return jsonify({'token': token})
            except Exception as _:
                return make_response('User already registered!', 401)

        @self.__app.route('/history-data')
        @self.token_required
        def get_history_data(current_user):
            stock_name = request.args.get('stock')
            history_data = self.__stock_data_service.get_history_data_for_certain_stock(stock_name)
            json_history_data = [h.to_json() for h in history_data]
            json_history_data_str = json.dumps(json_history_data)
            return jsonify({'history_data': json_history_data_str})


if __name__ == '__main__':
    db_connection = DatabaseConnection(Constants.HOST, Constants.USERNAME, Constants.PASSWORD, Constants.DATABASE)

    user_repository = UserRepository(db_connection)
    generated_prediction_repository = GeneratedPredictionRepository(db_connection)
    stock_data_repository = StockDataRepository(db_connection)

    apple_model = StockModel()
    amazon_model = StockModel()
    google_model = StockModel()
    microsoft_model = StockModel()

    apple_data = stock_data_repository.get_history_data_for_certain_stock('AAPL')
    apple_model.set_stock_data(apple_data)
    apple_model.buid_and_train_model()

    google_data = stock_data_repository.get_history_data_for_certain_stock('GOOG')
    google_model.set_stock_data(google_data)
    google_model.buid_and_train_model()

    amazon_data = stock_data_repository.get_history_data_for_certain_stock('AMZN')
    amazon_model.set_stock_data(amazon_data)
    amazon_model.buid_and_train_model()

    microsoft_data = stock_data_repository.get_history_data_for_certain_stock('MSFT')
    microsoft_model.set_stock_data(microsoft_data)
    microsoft_model.buid_and_train_model()

    user_service = UserService(user_repository)
    generated_prediction_service = GeneratedPredictionService(generated_prediction_repository, stock_data_repository)
    stock_data_service = StockDataService(stock_data_repository)
    stock_model_service = StockService(stock_data_repository, amazon_model, apple_model, google_model, microsoft_model)

    jobs = Job(stock_data_service, generated_prediction_service, apple_model, google_model, amazon_model, microsoft_model)
    jobs.run_jobs()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = Constants.SECRET_KEY
    CORS(app)
    controller = StockController(app, stock_model_service, stock_data_service, user_service, generated_prediction_service)
    app.run()