from flask import url_for
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

    def get_name(self):
        return self.__user['name'] if self.__user else "No name"

    def get_email(self):
        return self.__user['email'] if self.__user else 'No email'

    def get_avatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user['avatar']

        return img

    def verify_ext(self, filename):
        extension = filename.rsplit('.', 1)[1]
        if extension == 'png' or extension == 'PNG':
            return True
        else:
            return False


"""UserMixin were used instead"""

# def is_authenticated(self):
#     return True
#
# def is_active(self):
#     return True
#
# def is_anonymus(self):
#     return False
