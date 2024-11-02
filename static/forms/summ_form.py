from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, TextAreaField
from wtforms.validators import Length


class SummForm(FlaskForm):
    text = TextAreaField(
        "Текст",
        validators=[
            Length(
                max=1000000,
                message="Длина текста должна быть не более 1.000.000 символов.",
            )
        ],
    )
    type_of_sum = RadioField(choices=["Сильное сжатие", "Слабое сжатие"])
    submit = SubmitField("Сжать")
