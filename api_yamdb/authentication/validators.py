from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class LowercaseLettersUsernameValidator(validators.RegexValidator):
    """
    Validator for usernames.\n
    - Only ASCII lowercase letters, numbers and underscore are supported.
    - Must start with a letter.
    """
    regex = r'^[a-z][a-z0-9_]+$'
    message = (
        'Enter a valid username. This value may contain only '
        'lowercase ASCII letters, '
        'numbers, and underscores. Must start with a letter.'
    )
    flags = 0


@deconstructible
class NotMeUsername(validators.RegexValidator):
    """
    Userneme != 'Me'
    """
    regex = r'^(?!Me$|me$|ME$|mE$).*$'
    message = ('Userneme не может быть - Me')
    flags = 0
