from rest_framework import status
from rest_framework.exceptions import ValidationError

from api import constants


def validate_number(value) -> None:
    """Валидация минимального и максимального числа."""
    if constants.NUMBER_MAX < value < constants.NUMBER_MIN:
        raise ValidationError('Число не больше 32000 символов и не меньше 1',
                              code=status.HTTP_400_BAD_REQUEST)
