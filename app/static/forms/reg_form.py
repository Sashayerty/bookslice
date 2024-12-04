from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    password_again = PasswordField(validators=[DataRequired()])  # noqa
    name = StringField(validators=[DataRequired()])
    accept_using_conditions = BooleanField(
        "Принять",
        validators=[DataRequired("Соглашение с условием обязательно")],
    )
    submit = SubmitField("Регистрация")
