from django import forms
from walletapp.models import CustomUser

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