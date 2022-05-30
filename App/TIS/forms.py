from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["last_name", "first_name", "patronymic", "username", "email", "password", "num_group"]

        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=150)
    password = forms.CharField(label="Пароль", max_length=128, widget=forms.PasswordInput())
