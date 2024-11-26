from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class SumByIdForm(FlaskForm):
    type_of_sum = RadioField(
        choices=["Сильное сжатие", "Слабое сжатие"],
        validators=[DataRequired()],
    )
    submit = SubmitField(
        "Сжать",
    )
