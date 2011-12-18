# -* - coding: utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
import datetime

from person.models import User
from product.models import Product

class ReportForm(forms.Form):
    userModel = User()
    startdate = datetime.date(day=1, month=datetime.date.today().month, year=datetime.date.today().year)
    enddate = datetime.date.today()

    this_year = datetime.date.today().year
    years = range(2007, this_year + 1)

    start_date = forms.DateField(widget=SelectDateWidget(years=years), initial=startdate, label='data początkowa')
    end_date = forms.DateField(widget=SelectDateWidget(years=years), initial=enddate, label='data końcowa')
    warranty = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), choices=Product.WARRANTY_CHOICES, label='gwarancja')
    user = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), choices=userModel.get_user_choices(), label='pracownik')
    all_users = forms.BooleanField(label='wszyscy', required=False)
