from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    message = StringField(validators=[DataRequired()])
    send = SubmitField("Отправить")
