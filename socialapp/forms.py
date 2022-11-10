from django import forms
from django.contrib.auth.forms import UserCreationForm
from socialapp.models import Myuser, Posts, UserProfile

class RegistrationForm(UserCreationForm):
  first_name  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'First Name'}), label='')
  last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Last Name'}), label='')
  email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 
  'placeholder': 'Email'}), label='')
  username  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Username'}), label='')

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Password'}), label='')
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Confirm Password'}), label='')
  class Meta:
    model = Myuser
    fields = ['first_name', 'last_name', 'email', 
    'username', 'password1', 'password2']


class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 
  'placeholder': 'Username'}), label='')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 
  'placeholder': 'Password'}), label='')


class ProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ['bio', 'mobile', 'dob', 'gender']
    widgets = {
      'bio': forms.Textarea(attrs={'class': 'form-control', 'required':'true'}),
      'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
      'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'date of birth'}),
      'gender': forms.Select(attrs={'class': 'form-control'})
    }


class ProfilePicChangeForm(forms.ModelForm):
  class Meta:
    model = Myuser
    fields = ['profile_pic']