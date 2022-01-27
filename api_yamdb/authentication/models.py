from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.settings import ROLE, GLOBAL_SETTINGS
from .validators import NotMeUsername


class User(AbstractUser):

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text=(
            'Enter a valid username. This value may contain only '
            'lowercase ASCII letters, '
            'numbers, and underscores. Must start with a letter.'
        ),
        validators=[UnicodeUsernameValidator(), NotMeUsername()],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField('email address', unique=True,)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль - права доступа',
        max_length=10,
        choices=ROLE,
        default=GLOBAL_SETTINGS['user']
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Юзеры'
        verbose_name = 'Юзер'

    @property
    def _is_admin(self):
        return self.role == GLOBAL_SETTINGS['admin'] or self.is_superuser

    @property
    def _is_moderator(self):
        return self.role == GLOBAL_SETTINGS['moderator'] or self._is_admin
