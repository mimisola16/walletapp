from .models import *


from django import forms


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(decimal_places=2, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': '', 'class':'form-control',}))
    max_price = forms.DecimalField(decimal_places=2, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': '', 'class':'form-control',}))
    
    model = Product