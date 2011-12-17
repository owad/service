# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.forms.widgets import HiddenInput, Select
from django.forms import ChoiceField

from product.models import Product, Comment, Courier, File

class ProductForm(ModelForm):
    class Meta:
        model = Product
        widgets = {
            'client': HiddenInput(),
            'user': HiddenInput(),
            'status': HiddenInput(attrs={'value': Product.FIRST_STATUS}),
            'courier': Select(choices=[(obj.id, obj) for obj in Courier.objects.all()])
        }
        exclude = ('parcel_number', 'external_service_name', 'courier', 'fixed_by')
    warranty = ChoiceField(choices=Product.WARRANTY_CHOICES, initial=Product.N, label='Gwarancja')
    
    def full_clean(self):
        ModelForm.full_clean(self)
        max_cost_errors = self._errors.get('max_cost')
        if not max_cost_errors:
            if 'warranty' in self.data and self.data['warranty'] == Product.N and float(self.data['max_cost']) <= 0.00:
                max_cost_errors = self._errors.setdefault("max_cost", ErrorList())
                max_cost_errors.append("Podaj maksymalny koszt naprawy")
        
        
class ProductStatusChangeForm(ProductForm):
    class Meta:
        model = Product

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.COMMENT})
        }
        exclude = ('hardware', 'status')
        
class StaffCommentForm(CommentForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.HARDWARE_ADD})
        }
        exclude = ('status',)
    
class CourierCommentForm(CommentForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.COMMENT})
        }
        exclude = ('hardware', 'status')
    
    courier = forms.ChoiceField(label="Kurier", choices=[(obj.id, obj) for obj in Courier.objects.all()])
    parcel_number = forms.CharField(label="Numer przesyłki", max_length=64)


class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = ('product', )