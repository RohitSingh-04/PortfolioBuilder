from typing import Any, Mapping
from django import forms
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

class RegistrationForm(forms.ModelForm):

    password = forms.PasswordInput(attrs={'class':'form-control'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password']
        REQUIRED_FIELDS = ['username']