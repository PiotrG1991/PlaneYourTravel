from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('re_password')
        if password1 is None or password2 is None or password1 != password2:
            raise ValidationError('Wpisano dwa różne hasła')
        return cleaned_data
