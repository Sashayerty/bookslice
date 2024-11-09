from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SumForm(FlaskForm):
    text = TextAreaField(
        "Текст",
        validators=[
            Length(
                max=1000000,
                message="Длина текста должна быть не более 1.000.000 символов.",
            ),
            DataRequired(),
        ],
    )
    type_of_sum = RadioField(choices=["Сильное сжатие", "Слабое сжатие"])
    submit = SubmitField("Сжать")
