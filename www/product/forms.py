# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.forms import ChoiceField, CharField

from product.models import Product, Comment, Courier

class ProductForm(ModelForm):
    class Meta:
        model = Product
        widgets = {
            'client': HiddenInput(),
            'user': HiddenInput(),
            'status': HiddenInput(attrs={'value': Product.FIRST_STATUS})
        }
        exclude = ('parcel_number', 'external_service_name', 'courier', 'fixed_by')
    warranty = ChoiceField(choices=Product.WARRANTY_CHOICES, initial=Product.N, label='Gwarancja')
    
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
        exclude = ('hardware',)

class StaffCommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.HARDWARE_ADD})
        }
        
class CourierCommentForm(CommentForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.COMMENT})
        }
        exclude = ('hardware',)

    courier = forms.ChoiceField(label="Kurier", choices=[(obj.id, obj) for obj in Courier.objects.all()])
    parcel_number = forms.CharField(label="Numer przesyłki", max_length=64)
    