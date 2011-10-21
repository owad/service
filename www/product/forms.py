# -* - coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.forms import ChoiceField, CharField

from product.models import Product, Comment

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

class HardwareCommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'product': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(attrs={'value': Comment.HARDWARE_ADD})
        }