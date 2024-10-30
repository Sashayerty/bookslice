from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
