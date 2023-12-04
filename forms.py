from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("E che za nah?")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=100, message="Tupit etpe!")])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Enter")


class SignUpForm(FlaskForm):
    name = StringField("Name: ", validators=[Length(min=1, max=100, message="Name should from 4 to 100 symbols")])
    email = StringField("Email: ", validators=[Email("Incorrect email")])
    password = PasswordField("Password: ",
                             validators=[DataRequired(), Length(min=4, max=100, message="Long password must be")])
    password_repeat = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password', message="Passwords do not match.")])
    submit = SubmitField('Submit')