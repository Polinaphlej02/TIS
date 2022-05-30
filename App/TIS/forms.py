from django import forms
from .models import *


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["last_name", "first_name", "patronymic", "username", "email", "password", "num_group"]

        widgets = {
            'password': forms.PasswordInput(),
        }
