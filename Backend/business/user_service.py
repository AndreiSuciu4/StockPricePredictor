from werkzeug.security import generate_password_hash, check_password_hash

from Backend.Licenta.entity.user import User


class UserService:
    def __init__(self, user_repository):
        self.__user_repository = user_repository

    def login(self, email, password):
        user = self.__user_repository.find_user_by_email(email)
        if user is None:
            raise Exception("Invalid data!")
        else:
            if not check_password_hash(user.get_password(), password):
                raise Exception("Invalid data!")
        return user

    def register(self, firstname, lastname, email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(firstname, lastname, email, hashed_password)
        try:
            self.__user_repository.add_user(user)
        except Exception as _:
            raise Exception("User already registered!")

    def find_user_by_email(self, email):
        return self.__user_repository.find_user_by_email(email)
