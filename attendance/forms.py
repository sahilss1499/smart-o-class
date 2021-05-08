from django.forms import ModelForm
from django import forms

from .models import *

class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=70, min_length=4)
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'confirm_password']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=70)
    class Meta:
        fields = ['email', 'password']

# form for a teacher to add a batch
class BatchCreationForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'meet_link']