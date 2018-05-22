import re
from .expections import ValidationError


def validate(pattern, string):
    if not re.match(pattern, string):
        raise ValidationError(f'Fail to match {string}, pattern : {pattern}')
