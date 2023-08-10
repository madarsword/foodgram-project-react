import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>'
        )
    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError(
            f'Недопустимые символы <{value}> в имени пользователя'
        )
