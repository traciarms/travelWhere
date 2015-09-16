from django.core.exceptions import ValidationError
import re


def validate_zip_code(value):
    """
        This method will validate the zip code entered by the user
        :param value:
        :return:
    """
    match = re.search(r'^\d{5}(?:\-\d{4})?$', value)

    if not match:
        raise ValidationError(u'%s is not a valid zip code' % value)
