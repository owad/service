# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from person.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client

    def clean_phone_number(self):
        num_len = len(str(self.cleaned_data['phone_number']))
        if num_len != 9 and num_len != 0:
            if 'phone_number' not in self._errors:
                self._errors['phone_number'] = []
            self._errors['phone_number'].append('Błędny numer telefonu')
