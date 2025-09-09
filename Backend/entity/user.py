class User:
    def __init__(self, firstname, lastname, email, password):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__password = password

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_firstname(self):
        return self.__firstname

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def get_lastname(self):
        return self.__lastname

    def set_lastname(self, lastname):
        self.__lastname = lastname
