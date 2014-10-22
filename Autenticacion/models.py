# -*- coding: utf-8 -*-
__author__ = 'Elio Clímaco'

import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.core import validators
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError(_('Ingrese un nombre de usuario'))

        email = self.normalize_email(email)

        user = self.model\
        (
            username=username, email=email,
            is_staff=is_staff, is_active=False,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField\
    (
        _('username'), max_length=30, unique=True,
        help_text=_(u'Ingrese al menos 30 caracteres, entre letras, números y caracteres @/./+/-/_'),
        validators=
        [
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Ingrese un nombre de usuario válido.'), _('invalid'))
        ]
    )

    first_name  = models.CharField(_('first name'), max_length=30, blank=True, null=True)

    last_name   = models.CharField(_('last name'), max_length=30, blank=True, null=True)

    email       = models.EmailField(_('email address'), max_length=255)

    is_staff    = models.BooleanField\
    (
        _('staff status'), default=False,
        help_text=_(u'Designa si el usuario puede logearse en el sitio de administración.')
    )

    is_active   = models.BooleanField\
    (
        _('active'), default=False,
        help_text=_(u'Designa si el usuario debe ser considerado como activo. Deseleccione esto para eliminar las cuentas de usuario.')
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
    celular = models.CharField(max_length=10)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    # Vinculando el modelo Usuario, con
    # su clase manager.
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' %(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])