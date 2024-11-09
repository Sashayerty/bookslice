from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class SumByIdForm(FlaskForm):
    type_of_sum = RadioField(choices=["Сильное сжатие", "Слабое сжатие"])
    submit = SubmitField("Сжать")
