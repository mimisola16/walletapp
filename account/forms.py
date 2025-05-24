from django import forms
from walletapp.models import *
from django.contrib.auth.forms import SetPasswordForm
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_OPTIONS, required=False)
    user_type = forms.ChoiceField(choices=CustomUser.USERTYPE_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ('user_name', 'email', 'password', 'password2', 'profile_picture', 'gender', 'user_type')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = CustomUser.objects.filter(user_name=user_name)
        if r.exists():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
        self.fields['profile_picture'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['gender'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['user_type'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        
class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname',}))

    first_name = forms.CharField(
        label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    last_name = forms.CharField(
        label='Last Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    last_name = forms.CharField(
        label='Last Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'first_name', 'last_name',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class ProfileUpdateForm(forms.ModelForm):
    class Meta():
     
        model = CustomUser

        fields = ['profile_picture']
    
    
    
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-newpass'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Repeat Password', 'id': 'form-new-pass2'}))



class AddUserForm(forms.ModelForm):


    class Meta():
     
        model = CustomUser

        fields ='__all__'

        exclude = ['last_login']


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'shop_name', 'slug', 'address', 'email', 'shop_image', 
            'instagram', 'phone_number', 'shop_bio', 'category', 
            'appear_home', 'featured_shop', 'popular_shop',
            'monday_start_time', 'monday_end_time', 
            'tuesday_start_time', 'tuesday_end_time',
            'wednesday_start_time', 'wednesday_end_time',
            'thursday_start_time', 'thursday_end_time',
            'friday_start_time', 'friday_end_time',
            'saturday_start_time', 'saturday_end_time',
            'sunday_start_time', 'sunday_end_time'
        ]

        widgets = {
            'shop_bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Unique identifier for the shop', 'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'https://', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+1234567890', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields not explicitly styled
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'



class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'shop_name', 'category', 'product_image1', 'product_name', 
            'slug', 'price', 'no_of_stock', 'in_stock', 'content', 
            'best_seller_product', 'hot_trend'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'slug': forms.TextInput(attrs={'placeholder': 'Unique identifier for the product'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields not explicitly styled
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'
