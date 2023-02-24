from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model =User 
        fields = ['username','email','password1','password2']   

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full px-4 py-2 border rounded-lg appearance-none focus:outline-none focus:shadow-outline-gray','placeholder':'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full px-4 py-2 border rounded-lg appearance-none focus:outline-none focus:shadow-outline-gray','placeholder':'Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full px-4 py-2 border rounded-lg appearance-none focus:outline-none focus:shadow-outline-gray','placeholder':'Create Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full px-4 py-2 border rounded-lg appearance-none focus:outline-none focus:shadow-outline-gray','placeholder':'Confirm Password'}))
