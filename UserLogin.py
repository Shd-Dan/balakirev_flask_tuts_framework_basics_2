from flask_login import UserMixin


class UserLogin(UserMixin):
    # Responsible for getting user data by creating object UserLogin in decorator .user_loader
    # get_user() located in FDataBase class
    def from_data_base(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    # It's supporting method after authorization of user, in UserLogin user to fetch data, user - email
    # as argument fetched from database used in login()
    def create(self, user):
        self.__user = user
        return self

    def get_id_db(self):
        return str(self.__user['id'])

    # Implement the get_id method as required by Flask-Login
    def get_id(self):
        return str(self.__user['id'])

"""UserMixin were used instead"""


# def is_authenticated(self):
#     return True
#
# def is_active(self):
#     return True
#
# def is_anonymus(self):
#     return False


