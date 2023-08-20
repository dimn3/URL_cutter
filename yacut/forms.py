from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .consts import ORIGINAL_LINK_LENGTH, SHORT_LENGTH, SHORT_REXEXP
from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(),
            Length(max=ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=SHORT_LENGTH),
            Regexp(SHORT_REXEXP, message='Допустимы символы из латиницы и цифр'),
            Optional(),
        ]
    )
    submit = SubmitField('Добавить')

    def validate_custom_id(form, field):
        if URLMap.get(field.data):
            raise ValidationError(
                'Имя {0} уже занято!'.format(field.data)
            )
