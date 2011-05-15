# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms import ChoiceField, CharField
from django.forms.widgets import HiddenInput, CheckboxSelectMultiple, SelectMultiple
from www.service.models import Product, Comment, Client, User
from django.forms.extras.widgets import SelectDateWidget
import datetime

class ProductForm(ModelForm):
    class Meta:
        model = Product
        widgets = {
            'client': HiddenInput(),
            'user': HiddenInput(),
            'status': HiddenInput(attrs={'value': Product.FIRST_STATUS})
        }
    warranty = ChoiceField(choices=Product.WARRANTY_CHOICES, initial=Product.N, label='Gwarancja')
    
class ProductStatusChangeForm(ProductForm):
    id = CharField(widget=HiddenInput())
    class Meta:
        model = Product
        fields = ('id',)
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput()
        }

class ClientForm(ModelForm):
    class Meta:
        model = Client

class ReportForm(forms.Form):
    userModel = User()
    startdate = datetime.date(day=1, month=datetime.date.today().month, year=datetime.date.today().year)
    enddate = datetime.date.today()

    this_year = datetime.date.today().year
    years = range(2007, this_year + 1)

    start_date = forms.DateField(widget=SelectDateWidget(years=years), initial=startdate, label='data początkowa')
    end_date = forms.DateField(widget=SelectDateWidget(years=years), initial=enddate, label='data końcowa')
    warranty = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), choices=Product.WARRANTY_CHOICES, label='gwarancja')
    user = forms.MultipleChoiceField(widget=SelectMultiple(), choices=userModel.get_user_choices(), label='pracownik')
    
