from django import forms
from django.contrib.auth.forms import UserCreationForm
from socialapp.models import Myuser, Posts

class RegistrationForm(UserCreationForm):
  first_name  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'First Name'}), label='')
  last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Last Name'}), label='')
  email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 
  'placeholder': 'Email'}), label='')
  username  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Username'}), label='')
  profile_pic = forms.CharField(widget=forms.FileInput(attrs={'class': 'form-control'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Password'}), label='')
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Confirm Password'}), label='')
  class Meta:
    model = Myuser
    fields = ['first_name', 'last_name', 'email', 
    'username', 'profile_pic', 'password1', 'password2']


class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Username'}), label='')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Password'}), label='')
