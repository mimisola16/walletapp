from .models import *
from django import forms
from django.core.validators import EmailValidator 


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(decimal_places=2, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': '', 'class':'form-control',}))
    max_price = forms.DecimalField(decimal_places=2, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': '', 'class':'form-control',}))
    
    model = Products
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(validators=[EmailValidator()])
    phone = forms.CharField(max_length=15)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    
   