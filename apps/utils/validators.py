from django.core.exceptions import ValidationError
import re


def validate_phone(mobile):
    match = re.match(r'^(09)?\d{9}$', mobile)
    if not match:
        raise ValidationError('mobile number not valid')
