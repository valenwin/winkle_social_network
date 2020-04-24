from django import forms
from django.contrib.auth.models import User
from django_registration.forms import RegistrationFormUniqueEmail

from .utils import hunter, clearbit_signup
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password',
               'autocomplete': 'off', 'name': 'password', 'data-toggle': 'password'}
    ))


class RegistrationForm(RegistrationFormUniqueEmail):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        response = hunter.email_verifier(email)
        if response['result'] == 'undeliverable':
            raise forms.ValidationError('Email does not exist.')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.first_name = clearbit_signup(user.email)[0]
        user.last_name = clearbit_signup(user.email)[1]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Select a file 120x120')

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
