from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2']



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg form-control-alt',
        'placeholder': 'Your Email Address',
        'type': 'email',
        'name': 'email',
		'required':'required',
		'autofocus':'autofocus'
        }))
class UserNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserNewPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg form-control-alt',
        'placeholder': 'Enter New Password',
        'type': 'password',
        'name': 'new_password1',
		'required':'required',
		'autofocus':'autofocus'
        }))

    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg form-control-alt',
        'placeholder': 'Confirm New Password',
        'type': 'password',
        'name': 'new_password2',
		'required':'required',
        }))