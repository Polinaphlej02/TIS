from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["last_name", "first_name", "patronymic", "username", "email", "password", "num_group"]

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super(AddStudent, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=150)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class StudentAnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerStudent
        fields = "__all__"
