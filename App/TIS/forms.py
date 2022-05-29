from django import forms
from .models import *


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["surname", "name", "password", "num_group"]

        widgets = {
            'password': forms.PasswordInput(),
        }
