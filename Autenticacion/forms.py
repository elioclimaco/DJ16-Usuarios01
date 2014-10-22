#-*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django import forms
from .models import User


class UserCreationForm(AuthUserCreationForm):
    receive_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User

    # Este método esta definido en:
    # django.contrib.auth.form.UserCreationForm y
    # explícitamente enlaza a:
    # auth.models.User
    # así que necesitamos sobreescribirlo.

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError\
        (
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class UserChangeForm(AuthUserCreationForm):
    receive_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
