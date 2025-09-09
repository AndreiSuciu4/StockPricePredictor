import mysql
import mysql.connector


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.connection.commit()

    def executemany(self, query, values=None):
        self.cursor.executemany(query, values)
        self.connection.commit()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result
