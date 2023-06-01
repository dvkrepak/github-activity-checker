import re
from django.core.exceptions import ValidationError


def validate_respond_structure(respond):
    """
    Validates the structure of the 'respond' field in PullRequestMetrics model.

    This function validates whether the 'respond' field value adheres to the expected structure.
    The expected format is "<int> days, <int:2>:<int:2>:<int:2>".

    :param respond: The value of the 'respond' field to be validated.
    :raises ValidationError: If the 'respond' field value does not match the expected structure.
    :return: None
    """
    pattern = r'^\d+ days, \d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, respond):
        raise ValidationError('Invalid respond structure.\nUsage: <int> days, <int:2>:<int:2>:<int:2>')
