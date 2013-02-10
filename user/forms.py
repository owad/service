# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.core.validators import ValidationError

from user.models import User
from time import time


class UserForm(ModelForm):

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise ValidationError('To pole jest wymagane.')

        if User.objects.filter(username=username).exists() and not self.instance.pk:
            raise ValidationError('Taki użytkownik już istnieje.')

        return username

