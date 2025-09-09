from Backend.Licenta.entity.user import User


class UserRepository:
    def __init__(self, database_connection):
        self._db_connection = database_connection

    def add_user(self, user):
        query = "INSERT INTO user (email, password, firstname, lastname) VALUES (%s, %s, %s, %s)"
        values = (user.get_email(), user.get_password(), user.get_firstname(), user.get_lastname())
        with self._db_connection as cursor:
            cursor.execute_query(query, values)

    def find_user_by_email(self, email):
        query = "SELECT * FROM user WHERE email = %s"
        values = (email,)
        with self._db_connection as cursor:
            result = cursor.fetch_one(query, values)

        if result is not None:
            user = User(result[1], result[2], result[3], result[4])
            return user
        else:
            return None
